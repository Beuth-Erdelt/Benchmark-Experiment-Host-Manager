"""
Load one delimited file into one table of IBM Db2 (bexhoma loader).

Usage: python3 load.py <table> <file>

The file is sent by the client (remote external table, REMOTESOURCE 'YES' of the
IBM Data Server Driver of ibm_db): INSERT INTO <table> SELECT * FROM EXTERNAL
'<file>'. It is loaded in chunks of DB2_LOAD_CHUNK_ROWS lines, one transaction
(autocommit) per chunk, so the transaction log of the server needs room for
one chunk per loader only. Db2 rejects a statement whose file has a bad row
(MaxErrors 1), so a chunk is either loaded completely or not at all.

A chunk is retried (DB2_LOAD_RETRIES times, 5 s apart) only on errors that mean
no connection (communication errors, database not yet active); a chunk that
fails otherwise ends the file. The last line of the output is
"BEXHOMA_LOADED:<rows>" with the number of rows Db2 reports as inserted; the
exit code is 0 if all chunks were loaded, 1 otherwise.

Environment: BEXHOMA_HOST, BEXHOMA_PORT, BEXHOMA_DATABASE, BEXHOMA_USER,
BEXHOMA_PASSWORD, BEXHOMA_SCHEMA (optional, else the default schema of the
user), DB2_DELIMITER (default '|'), DB2_EMPTY_AS_NULL (1: an empty field is
NULL, as in TPC-DS; default 0: an empty field of a character column is an empty
string), DB2_LOAD_CHUNK_ROWS (default 200000), DB2_LOAD_RETRIES (default 10).

Author: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
"""
import os
import sys
import time

import ibm_db

# SQLSTATE classes of errors after which a retry may succeed: 08 connection
# exception, 57019/57011/57033 database not started or resources unavailable
TRANSIENT_SQLSTATES = ('08', '57019', '57011', '57033', '40003')


def connection_string():
    return ("DATABASE={db};HOSTNAME={host};PORT={port};PROTOCOL=TCPIP;UID={user};PWD={pwd};"
            .format(db=os.environ.get('BEXHOMA_DATABASE', 'bexhoma'),
                    host=os.environ.get('BEXHOMA_HOST', 'localhost'),
                    port=os.environ.get('BEXHOMA_PORT', '50000'),
                    user=os.environ.get('BEXHOMA_USER', 'db2inst1'),
                    pwd=os.environ.get('BEXHOMA_PASSWORD', '')))


def is_transient(message):
    state = ''
    if 'SQLSTATE=' in message:
        state = message.split('SQLSTATE=')[1][:5]
    return state.startswith(TRANSIENT_SQLSTATES) or 'SQL30081N' in message or 'SQL1224N' in message


def connect():
    conn = ibm_db.connect(connection_string(), '', '')
    schema = os.environ.get('BEXHOMA_SCHEMA', '')
    if schema:
        ibm_db.exec_immediate(conn, 'SET SCHEMA "{}"'.format(schema.upper()))
    return conn


def load_chunk(conn, table, chunk_file, delimiter):
    nullvalue = " NULLVALUE ''" if os.environ.get('DB2_EMPTY_AS_NULL', '0') == '1' else ''
    sql = ("INSERT INTO {table} SELECT * FROM EXTERNAL '{file}' "
           "USING (DELIMITER '{delim}' REMOTESOURCE 'YES' MAXERRORS 1{nullvalue})"
           .format(table=table, file=chunk_file, delim=delimiter, nullvalue=nullvalue))
    stmt = ibm_db.exec_immediate(conn, sql)
    return ibm_db.num_rows(stmt)


def chunks(path, size, tmpdir):
    """Yield (chunk file, number of lines) of at most size lines each."""
    with open(path, 'rb') as source:
        number = 0
        while True:
            lines = []
            for line in source:
                lines.append(line)
                if len(lines) >= size:
                    break
            if not lines:
                return
            number += 1
            chunk_file = os.path.join(tmpdir, 'bexhoma-chunk-{}-{}'.format(os.getpid(), number))
            with open(chunk_file, 'wb') as target:
                target.writelines(lines)
            yield chunk_file, len(lines)
            if len(lines) < size:
                return


def main():
    table, path = sys.argv[1], sys.argv[2]
    delimiter = os.environ.get('DB2_DELIMITER', '|')
    size = int(os.environ.get('DB2_LOAD_CHUNK_ROWS', '200000'))
    retries = int(os.environ.get('DB2_LOAD_RETRIES', '10'))
    tmpdir = os.path.dirname(os.path.abspath(path))
    loaded = 0
    ok = True
    conn = None
    for chunk_file, lines in chunks(path, size, tmpdir):
        attempt = 0
        while True:
            attempt += 1
            try:
                if conn is None:
                    conn = connect()
                rows = load_chunk(conn, table, chunk_file, delimiter)
                loaded += rows
                if rows != lines:
                    print('chunk {}: {} lines, {} rows inserted'.format(chunk_file, lines, rows), flush=True)
                    ok = False
                break
            except Exception as e:
                message = str(e)
                print('ERROR: chunk {} attempt {}: {}'.format(chunk_file, attempt, message), flush=True)
                if conn is not None and not is_transient(message):
                    ok = False
                    break
                if attempt >= retries:
                    ok = False
                    break
                try:
                    if conn is not None:
                        ibm_db.close(conn)
                except Exception:
                    pass
                conn = None
                time.sleep(5)
        os.remove(chunk_file)
        if not ok:
            break
    if conn is not None:
        ibm_db.close(conn)
    print('BEXHOMA_LOADED:{}'.format(loaded), flush=True)
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
