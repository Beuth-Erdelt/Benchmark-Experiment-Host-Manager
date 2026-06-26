"""
Shared argument parser factory for bexhoma CLI scripts.

Provides :func:`make_base_parser`, which returns an :class:`argparse.ArgumentParser`
pre-loaded with all arguments that are common to ``benchbase.py``, ``hammerdb.py``,
``tpch.py``, ``tpcds.py``, and ``ycsb.py``.

Authors: Patrick K. Erdelt
Copyright (C) 2023 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import argparse


def make_base_parser():
    """
    Returns an :class:`~argparse.ArgumentParser` (with ``add_help=False``) pre-loaded
    with all arguments common to the bexhoma benchmark entry-point scripts.

    Intended to be passed as a parent::

        parser = argparse.ArgumentParser(parents=[make_base_parser()], ...)

    Standardised defaults that differ from some of the original per-script
    values:

    - ``--timeout`` → ``600``
    - ``--request-gpu-type`` → ``''``
    - ``--num-worker`` → ``0``  (use ``parser.set_defaults(num_worker=1)`` to override)

    :return: Argument parser carrying all shared arguments.
    :rtype: argparse.ArgumentParser
    """
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument('-aws', '--aws', help='pin components to AWS EKS node groups', action='store_true', default=False)
    p.add_argument('-db',  '--debug', help='enable debug logging', action='store_true')
    p.add_argument('-sl',  '--skip-loading', help='skip data loading and start benchmarking immediately', action='store_true', default=False)
    p.add_argument('-ss',  '--skip-shutdown', help='keep SUT pods running after the experiment finishes', action='store_true', default=False)
    p.add_argument('-cx',  '--context', help='kubectl context to use (default: current context)', default=None)
    p.add_argument('-e',   '--experiment', help='resume an existing experiment by its code', default=None)
    p.add_argument('-m',   '--monitoring', help='enable Prometheus monitoring for the SUT', action='store_true')
    p.add_argument('-ma',  '--monitoring-app', help='enable application-level metrics collection', action='store_true', default=False)
    p.add_argument('-mc',  '--monitoring-cluster', help='enable node-level monitoring for the entire cluster', action='store_true', default=False)
    p.add_argument('-ms',  '--max-sut', help='maximum number of DBMS configurations to run in parallel cluster-wide (default: no limit)', default=None)
    p.add_argument('-mse', '--max-sut-experiment', help='maximum number of DBMS configurations in this experiment to run in parallel (default: no limit)', default=None)
    p.add_argument('-nc',  '--num-config', help='number of experiment repetitions per configuration', default=1)
    p.add_argument('-ne',  '--num-query-executors', help='comma-separated list of parallel client counts to sweep', default="1")
    p.add_argument('-nw',  '--num-worker', help='number of worker nodes for distributed DBMS', default=0)
    p.add_argument('-nwr', '--num-worker-replicas', help='number of replicas per worker node', default=0)
    p.add_argument('-nws', '--num-worker-shards', help='number of shards per worker node', default=0)
    p.add_argument('-nlp', '--num-loading-pods', help='comma-separated list of total loader pod counts', default="1")
    p.add_argument('-nlt', '--num-loading-threads', help='comma-separated list of total loader threads (split across pods)', default="1")
    p.add_argument('-nbp', '--num-benchmarking-pods', help='comma-separated list of benchmarker pod counts', default="1")
    p.add_argument('-nbt', '--num-benchmarking-threads', help='total benchmarking threads, split evenly across pods', default="1")
    p.add_argument('-sf',  '--scaling-factor', help='scaling factor controlling dataset size', default=1)
    p.add_argument('-t',   '--timeout', help='per-query timeout in seconds', default=600)
    p.add_argument('-lr',  '--limit-ram', help='RAM limit for the SUT and worker pods (e.g. 64Gi; 0 = no limit)', default='0')
    p.add_argument('-lc',  '--limit-cpu', help='CPU limit for the SUT and worker pods (e.g. 4; 0 = no limit)', default='0')
    p.add_argument('-rr',  '--request-ram', help='RAM request for the SUT and worker pods (e.g. 16Gi)', default='16Gi')
    p.add_argument('-rc',  '--request-cpu', help='CPU request for the SUT and worker pods (e.g. 4)', default='4')
    p.add_argument('-rct', '--request-cpu-type', help='require SUT node to carry label cpu=<value>', default='')
    p.add_argument('-rg',  '--request-gpu', help='number of GPUs to request for the SUT pod', default=1)
    p.add_argument('-rgt', '--request-gpu-type', help='require SUT node to carry label gpu=<value>', default='')
    p.add_argument('-rst', '--request-storage-type', help='storage class for the SUT persistent volume', default=None, choices=[None, '', 'local-hdd', 'shared', 'ramdisk', 'cephcsi'])
    p.add_argument('-rss', '--request-storage-size', help='size of the SUT persistent volume (e.g. 10Gi)', default='')
    p.add_argument('-rsr', '--request-storage-remove', help='delete any existing PVC for the SUT before starting', action='store_true', default=False)
    p.add_argument('-rnn', '--request-node-name', help='pin the SUT pod to this Kubernetes node', default=None)
    p.add_argument('-rnl', '--request-node-loading', help='pin loader pods to this Kubernetes node', default=None)
    p.add_argument('-rnb', '--request-node-benchmarking', help='pin benchmarker pods to this Kubernetes node', default=None)
    p.add_argument('-mtn', '--multi-tenant-num', help='number of tenants for multi-tenant experiments', default=0)
    p.add_argument('-mtb', '--multi-tenant-by', help='tenancy granularity: schema, database, or container', default='')
    p.add_argument('-mtv', '--multi-tenant-volume', help='allocate a separate persistent volume per tenant', action='store_true', default=False)
    p.add_argument('-tr',  '--test-result', help='validate that results meet basic correctness requirements', action='store_true', default=False)
    p.add_argument("--set", dest="sets", action="append", default=[], help="override a deployment parameter, e.g. deployment[sut].container[dbms].max_worker_processes=128")
    return p
