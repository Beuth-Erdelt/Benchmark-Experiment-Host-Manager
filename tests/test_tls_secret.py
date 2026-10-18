"""
Tests for the SUT TLS Secret (bexhoma/tls.py).

MySQL 9 needs TLS for the first ``caching_sha2_password`` login; bexhoma
creates a CA and a server certificate per SUT, mounts them into the server
and gives HammerDB the CA. Covers the Secret document and the template patch
with TLS on and off.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import unittest

import yaml
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import padding

from bexhoma.tls import TLS_KEYS, TLS_VOLUME, apply_tls_volume, build_tls_secret, tls_dns_names


def _load(template):
    with open('k8s/' + template) as f:
        return [d for d in yaml.safe_load_all(f) if isinstance(d, dict)]


def _pod_spec(docs, kind):
    return next(d for d in docs if d.get('kind') == kind)['spec']['template']['spec']


class TlsSecretTest(unittest.TestCase):
    """The generated Secret: name, labels, keys, SANs, CA signature."""

    @classmethod
    def setUpClass(cls):
        cls.labels = {'app': 'bexhoma', 'component': 'tls', 'configuration': 'MySQL-1', 'experiment': '123'}
        cls.secret = build_tls_secret('bexhoma-tls-mysql-1-123', 'bexhoma-sut-mysql-1-123', 'perdelt', cls.labels)

    def test_document(self):
        self.assertEqual(self.secret['kind'], 'Secret')
        self.assertEqual(self.secret['metadata']['name'], 'bexhoma-tls-mysql-1-123')
        self.assertEqual(self.secret['metadata']['labels'], self.labels)
        self.assertEqual(set(self.secret['stringData']), set(TLS_KEYS))
        self.assertIn('PRIVATE KEY', self.secret['stringData']['server-key.pem'])

    def test_server_certificate(self):
        ca = x509.load_pem_x509_certificate(self.secret['stringData']['ca.pem'].encode())
        cert = x509.load_pem_x509_certificate(self.secret['stringData']['server-cert.pem'].encode())
        sans = cert.extensions.get_extension_for_class(x509.SubjectAlternativeName).value
        self.assertEqual(sans.get_values_for_type(x509.DNSName), tls_dns_names('bexhoma-sut-mysql-1-123', 'perdelt'))
        self.assertIn('bexhoma-sut-mysql-1-123.perdelt.svc.cluster.local', sans.get_values_for_type(x509.DNSName))
        self.assertEqual(cert.issuer, ca.subject)
        ca.public_key().verify(cert.signature, cert.tbs_certificate_bytes, padding.PKCS1v15(),
                               cert.signature_hash_algorithm)
        self.assertTrue(ca.extensions.get_extension_for_class(x509.BasicConstraints).value.ca)
        self.assertFalse(cert.extensions.get_extension_for_class(x509.BasicConstraints).value.ca)

    def test_fresh_material_per_call(self):
        other = build_tls_secret('x', 'bexhoma-sut-mysql-1-123', 'perdelt')
        self.assertNotEqual(other['stringData']['ca.pem'], self.secret['stringData']['ca.pem'])
        self.assertEqual(other['metadata']['labels'], {})

    def test_long_service_name(self):
        secret = build_tls_secret('x', 's' * 80, 'ns')
        cert = x509.load_pem_x509_certificate(secret['stringData']['server-cert.pem'].encode())
        self.assertTrue(cert.subject)


class ApplyTlsVolumeTest(unittest.TestCase):
    """Templates: Secret name filled in with TLS on; volume, mounts and args removed with TLS off."""

    def test_mysql_on(self):
        spec = _pod_spec(_load('deploymenttemplate-MySQL.yml'), 'Deployment')
        self.assertTrue(apply_tls_volume(spec, 'bexhoma-tls-mysql-1-123'))
        vol = next(v for v in spec['volumes'] if v['name'] == TLS_VOLUME)
        self.assertEqual(vol['secret']['secretName'], 'bexhoma-tls-mysql-1-123')
        dbms = next(c for c in spec['containers'] if c['name'] == 'dbms')
        self.assertIn('--ssl-ca=/etc/mysql/certs/ca.pem', dbms['args'])

    def test_mysql_off(self):
        spec = _pod_spec(_load('deploymenttemplate-MySQL.yml'), 'Deployment')
        self.assertFalse(apply_tls_volume(spec, ''))
        self.assertNotIn(TLS_VOLUME, [v['name'] for v in spec['volumes']])
        dbms = next(c for c in spec['containers'] if c['name'] == 'dbms')
        self.assertNotIn(TLS_VOLUME, [m['name'] for m in dbms['volumeMounts']])
        self.assertFalse([a for a in dbms['args'] if a.startswith('--ssl-')])
        self.assertIn('--skip-log-bin', dbms['args'])

    def test_hammerdb_jobs(self):
        for template in ('jobtemplate-loading-hammerdb.yml', 'jobtemplate-benchmarking-hammerdb.yml'):
            spec = _pod_spec(_load(template), 'Job')
            self.assertTrue(apply_tls_volume(spec, 'sec'), template)
            vol = next(v for v in spec['volumes'] if v['name'] == TLS_VOLUME)
            self.assertEqual(vol['secret']['items'], [{'key': 'ca.pem', 'path': 'ca-cert.pem'}])
            spec = _pod_spec(_load(template), 'Job')
            self.assertFalse(apply_tls_volume(spec, None), template)
            self.assertNotIn(TLS_VOLUME, [v['name'] for v in spec['volumes'] or []])
            for c in spec['containers']:
                self.assertNotIn(TLS_VOLUME, [m['name'] for m in c.get('volumeMounts') or []])

    def test_template_without_tls_volume(self):
        spec = _pod_spec(_load('deploymenttemplate-PostgreSQL.yml'), 'Deployment')
        before = yaml.safe_dump(spec)
        self.assertFalse(apply_tls_volume(spec, 'sec'))
        self.assertFalse(apply_tls_volume(spec, ''))
        self.assertEqual(yaml.safe_dump(spec), before)


if __name__ == '__main__':
    unittest.main()
