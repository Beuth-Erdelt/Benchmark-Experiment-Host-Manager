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
    p.add_argument('-aws', '--aws', help='fix components to node groups at AWS', action='store_true', default=False)
    p.add_argument('-db',  '--debug', help='dump debug informations', action='store_true')
    p.add_argument('-sl',  '--skip-loading', help='do not ingest, start benchmarking immediately', action='store_true', default=False)
    p.add_argument('-ss',  '--skip-shutdown', help='do not remove SUTs after benchmarking', action='store_true', default=False)
    p.add_argument('-cx',  '--context', help='context of Kubernetes (for a multi cluster environment), default is current context', default=None)
    p.add_argument('-e',   '--experiment', help='sets experiment code for continuing started experiment', default=None)
    p.add_argument('-m',   '--monitoring', help='activates monitoring for sut', action='store_true')
    p.add_argument('-ma',  '--monitoring-app', help='activates application monitoring', action='store_true', default=False)
    p.add_argument('-mc',  '--monitoring-cluster', help='activates monitoring for all nodes of cluster', action='store_true', default=False)
    p.add_argument('-ms',  '--max-sut', help='maximum number of parallel DBMS configurations, default is no limit', default=None)
    p.add_argument('-nc',  '--num-config', help='number of runs per configuration', default=1)
    p.add_argument('-ne',  '--num-query-executors', help='comma separated list of number of parallel clients', default="1")
    p.add_argument('-nw',  '--num-worker', help='number of workers (for distributed dbms)', default=0)
    p.add_argument('-nwr', '--num-worker-replicas', help='number of workers replications (for distributed dbms)', default=0)
    p.add_argument('-nws', '--num-worker-shards', help='number of worker shards (for distributed dbms)', default=0)
    p.add_argument('-nlp', '--num-loading-pods', help='total number of loaders per configuration', default="1")
    p.add_argument('-nlt', '--num-loading-threads', help='total number of threads per loading process', default="1")
    p.add_argument('-nbp', '--num-benchmarking-pods', help='comma separated list of number of benchmarkers per configuration', default="1")
    p.add_argument('-nbt', '--num-benchmarking-threads', help='total number of threads per benchmarking process', default="1")
    p.add_argument('-sf',  '--scaling-factor', help='scaling factor (SF)', default=1)
    p.add_argument('-t',   '--timeout', help='timeout for a run of a query', default=600)
    p.add_argument('-lr',  '--limit-ram', help='limit ram for sut, default 0 (none)', default='0')
    p.add_argument('-lc',  '--limit-cpu', help='limit cpus for sut, default 0 (none)', default='0')
    p.add_argument('-rr',  '--request-ram', help='request ram for sut, default 16Gi', default='16Gi')
    p.add_argument('-rc',  '--request-cpu', help='request cpus for sut, default 4', default='4')
    p.add_argument('-rct', '--request-cpu-type', help='request node for sut to have node label cpu=', default='')
    p.add_argument('-rg',  '--request-gpu', help='request number of gpus for sut', default=1)
    p.add_argument('-rgt', '--request-gpu-type', help='request node for sut to have node label gpu=', default='')
    p.add_argument('-rst', '--request-storage-type', help='request persistent storage of certain type', default=None, choices=[None, '', 'local-hdd', 'shared', 'ramdisk'])
    p.add_argument('-rss', '--request-storage-size', help='request persistent storage of certain size', default='10Gi')
    p.add_argument('-rsr', '--request-storage-remove', help='remove existing persistent storage at experiment start', action='store_true', default=False)
    p.add_argument('-rnn', '--request-node-name', help='request a specific node for sut', default=None)
    p.add_argument('-rnl', '--request-node-loading', help='request a specific node for loading pods', default=None)
    p.add_argument('-rnb', '--request-node-benchmarking', help='request a specific node for benchmarking pods', default=None)
    p.add_argument('-mtn', '--multi-tenant-num', help='number of tenant', default=0)
    p.add_argument('-mtb', '--multi-tenant-by', help='one tenant per (schema, database, container)', default='')
    p.add_argument('-mtv', '--multi-tenant-volume', help='one volume per tenant per (for per-database)', action='store_true', default=False)
    p.add_argument('-tr',  '--test-result', help='test if result fulfills some basic requirements', action='store_true', default=False)
    p.add_argument("--set", dest="sets", action="append", default=[], help="Selector assignment, e.g. deployment[sut].container[dbms].max_worker_processes=128")
    return p
