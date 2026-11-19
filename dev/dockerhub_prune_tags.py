"""
Deletes the tags of all bexhoma/* repositories on Docker Hub whose version is older than a given one.

Kept: latest, and Bexhoma versions X.Y.Z (without v prefix) from the given version on.
Deleted: every other tag last updated before the repository's tag of that version, which
includes older Bexhoma versions and tool-version tags such as v0.14.16, dev, 0.17.0 or 4.12.
Other tags updated later are kept and listed. A repository without a tag of the given version
is skipped entirely, so no repository is emptied.

Dry run by default: lists what would be deleted. With --delete, the tags are deleted.
Deleting needs a Docker Hub personal access token with "Read, Write, Delete":

    DOCKERHUB_USER=... DOCKERHUB_TOKEN=... python dev/dockerhub_prune_tags.py --keep-from 0.11.18 --delete

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import argparse
import json
import os
import re
import sys
import urllib.request

API = 'https://hub.docker.com/v2'
VERSION = re.compile(r'v?(\d+)\.(\d+)\.(\d+)')


def request(url, method='GET', token=None, data=None):
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = 'Bearer ' + token
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(req) as response:
        text = response.read()
        return response.status, (json.loads(text) if text else None)


def paged(url, token=None):
    while url:
        _, page = request(url, token=token)
        yield from page['results']
        url = page['next']


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--namespace', default='bexhoma')
    parser.add_argument('--keep-from', default='0.11.18', help='oldest version to keep')
    parser.add_argument('--delete', action='store_true', help='delete; without it, only list')
    args = parser.parse_args()
    keep_from = tuple(int(x) for x in VERSION.fullmatch(args.keep_from).groups())

    token = None
    if args.delete:
        user, pat = os.environ.get('DOCKERHUB_USER'), os.environ.get('DOCKERHUB_TOKEN')
        if not user or not pat:
            sys.exit('set DOCKERHUB_USER and DOCKERHUB_TOKEN to delete')
        _, login = request(API + '/users/login/', 'POST', data={'username': user, 'password': pat})
        token = login['token']

    repos = sorted(r['name'] for r in paged(f'{API}/repositories/{args.namespace}/?page_size=100', token))
    total_delete = 0
    for repo in repos:
        tags = {t['name']: t['last_updated'] for t in paged(f'{API}/repositories/{args.namespace}/{repo}/tags?page_size=100', token)}
        if args.keep_from not in tags:
            print(f'{repo}: SKIPPED, no tag {args.keep_from} ({len(tags)} tags)')
            continue
        cutoff = tags[args.keep_from]

        def kept(tag):
            m = VERSION.fullmatch(tag)
            # a tool version such as YCSB's 0.17.0 also looks like a newer Bexhoma version,
            # so a version tag is kept only if it is not older than the cutoff tag
            return tag == 'latest' or (m and not tag.startswith('v') and tags[tag] >= cutoff
                                       and tuple(int(x) for x in m.groups()) >= keep_from)

        delete = sorted(t for t in tags if not kept(t) and tags[t] < cutoff)
        newer = [t for t in tags if not kept(t) and tags[t] >= cutoff]
        total_delete += len(delete)
        print(f'{repo}: delete {len(delete)}, keep {len(tags) - len(delete)}'
              + (f' (newer, not in the scheme, kept: {", ".join(newer)})' if newer else ''))
        if args.delete:
            for tag in delete:
                status, _ = request(f'{API}/repositories/{args.namespace}/{repo}/tags/{tag}/', 'DELETE', token)
                if status != 204:
                    print(f'  {repo}:{tag} -> HTTP {status}')
    print(f'{"Deleted" if args.delete else "Would delete"} {total_delete} tags in {len(repos)} repositories')


if __name__ == '__main__':
    main()
