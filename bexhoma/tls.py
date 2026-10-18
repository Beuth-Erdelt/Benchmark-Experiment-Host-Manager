"""
TLS material for a SUT: a self-signed CA plus a server certificate in a Secret.

MySQL 9 has no ``mysql_native_password``; ``caching_sha2_password`` needs TLS
(or the server's RSA key) for a client's first login, and HammerDB only does
TLS with a readable CA file. bexhoma therefore creates one Secret per SUT,
mounts it into the server and gives the clients the CA.

Templates declare where the Secret goes with a volume named
:data:`TLS_VOLUME`; :func:`apply_tls_volume` fills in the Secret name, or
removes the volume, its mounts and the ``--ssl-*`` args when TLS is off.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import datetime
import ipaddress
from typing import Optional

__all__ = [
    'TLS_VOLUME', 'TLS_COMPONENT', 'TLS_KEYS', 'TLS_ENV', 'TLS_SERVER_ARG_PREFIXES',
    'tls_dns_names', 'build_tls_secret', 'apply_tls_volume',
]

#: Name of the pod volume that carries the TLS Secret in a template.
TLS_VOLUME = 'bexhoma-tls'
#: ``component`` label of the Secret (cleanup selects it by this label).
TLS_COMPONENT = 'tls'
#: Keys of the Secret.
TLS_KEYS = ('ca.pem', 'server-cert.pem', 'server-key.pem')
#: Env var set to ``true`` in job containers that mount the CA.
TLS_ENV = 'BEXHOMA_TLS'
#: Server args that point into the TLS volume; removed together with it.
TLS_SERVER_ARG_PREFIXES = ('--ssl-ca=', '--ssl-cert=', '--ssl-key=', '--ssl_ca=', '--ssl_cert=', '--ssl_key=')

#: Validity of the generated certificates. A SUT never runs that long.
_VALIDITY_DAYS = 30
_RSA_KEY_SIZE = 2048


def tls_dns_names(service: str, namespace: str) -> list:
    """Return the DNS names a client may use to reach the SUT service.

    :param service: Name of the SUT service.
    :param namespace: Kubernetes namespace.
    :return: Service name, its namespace-qualified forms, and ``localhost``.
    :rtype: list[str]
    """
    return [
        service,
        f'{service}.{namespace}',
        f'{service}.{namespace}.svc',
        f'{service}.{namespace}.svc.cluster.local',
        'localhost',
    ]


def _pem_key(key) -> str:
    from cryptography.hazmat.primitives import serialization
    return key.private_bytes(
        serialization.Encoding.PEM, serialization.PrivateFormat.TraditionalOpenSSL,
        serialization.NoEncryption()).decode('ascii')


def _pem_cert(cert) -> str:
    from cryptography.hazmat.primitives import serialization
    return cert.public_bytes(serialization.Encoding.PEM).decode('ascii')


def build_tls_secret(name: str, service: str, namespace: str, labels: Optional[dict] = None) -> dict:
    """Generate a CA and a server certificate and return them as a Secret document.

    :param name: Name of the Secret.
    :param service: SUT service name; becomes the certificate's CN and SANs.
    :param namespace: Namespace of the SUT (for the qualified SANs).
    :param labels: Labels of the Secret.
    :return: Secret document with ``stringData`` keys :data:`TLS_KEYS`.
    :rtype: dict
    """
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID

    now = datetime.datetime.now(datetime.timezone.utc)
    not_before = now - datetime.timedelta(minutes=5)
    not_after = now + datetime.timedelta(days=_VALIDITY_DAYS)

    ca_key = rsa.generate_private_key(public_exponent=65537, key_size=_RSA_KEY_SIZE)
    # a CN holds at most 64 characters
    ca_name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, f'bexhoma CA {service}'[:64])])
    ca_cert = (
        x509.CertificateBuilder()
        .subject_name(ca_name).issuer_name(ca_name)
        .public_key(ca_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(not_before).not_valid_after(not_after)
        .add_extension(x509.BasicConstraints(ca=True, path_length=0), critical=True)
        .add_extension(x509.KeyUsage(
            digital_signature=True, key_cert_sign=True, crl_sign=True, content_commitment=False,
            key_encipherment=False, data_encipherment=False, key_agreement=False,
            encipher_only=False, decipher_only=False), critical=True)
        .sign(ca_key, hashes.SHA256())
    )

    server_key = rsa.generate_private_key(public_exponent=65537, key_size=_RSA_KEY_SIZE)
    sans = [x509.DNSName(n) for n in tls_dns_names(service, namespace)]
    sans.append(x509.IPAddress(ipaddress.ip_address('127.0.0.1')))
    server_cert = (
        x509.CertificateBuilder()
        .subject_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, service[:64])]))
        .issuer_name(ca_name)
        .public_key(server_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(not_before).not_valid_after(not_after)
        .add_extension(x509.SubjectAlternativeName(sans), critical=False)
        .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
        .add_extension(x509.ExtendedKeyUsage([ExtendedKeyUsageOID.SERVER_AUTH]), critical=False)
        .sign(ca_key, hashes.SHA256())
    )

    return {
        'apiVersion': 'v1',
        'kind': 'Secret',
        'type': 'Opaque',
        'metadata': {'name': name, 'labels': dict(labels or {})},
        'stringData': {
            'ca.pem': _pem_cert(ca_cert),
            'server-cert.pem': _pem_cert(server_cert),
            'server-key.pem': _pem_key(server_key),
        },
    }


def apply_tls_volume(pod_spec: dict, secret_name: Optional[str]) -> bool:
    """Point the template's TLS volume at the Secret, or remove it.

    With a ``secret_name``, every volume named :data:`TLS_VOLUME` gets
    ``secret.secretName``. Without one, those volumes are removed, together
    with their mounts and the containers' ``--ssl-ca/--ssl-cert/--ssl-key`` args.

    :param pod_spec: ``spec.template.spec`` of a Deployment, StatefulSet or Job.
    :param secret_name: Name of the Secret, or ``None``/``''`` when TLS is off.
    :return: True iff the pod spec mounts the Secret afterwards.
    :rtype: bool
    """
    volumes = pod_spec.get('volumes') or []
    tls_volumes = [v for v in volumes if isinstance(v, dict) and v.get('name') == TLS_VOLUME]
    if not tls_volumes:
        return False
    if secret_name:
        for v in tls_volumes:
            v.setdefault('secret', {})
            if v['secret'] is None:
                v['secret'] = {}
            v['secret']['secretName'] = secret_name
        return True
    pod_spec['volumes'] = [v for v in volumes if v not in tls_volumes]
    for key in ('containers', 'initContainers'):
        for c in pod_spec.get(key) or []:
            mounts = c.get('volumeMounts') or []
            if not any(m.get('name') == TLS_VOLUME for m in mounts):
                continue
            c['volumeMounts'] = [m for m in mounts if m.get('name') != TLS_VOLUME]
            if c.get('args'):
                c['args'] = [a for a in c['args']
                             if not (isinstance(a, str) and a.startswith(TLS_SERVER_ARG_PREFIXES))]
    return False
