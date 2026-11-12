"""
TPC-H refresh function RF2 for IBM Db2 (bexhoma refresh loader).

Usage: python3 rf2.py <delete file>

Deletes the lineitems and orders whose order keys are in the delete file, in one
transaction. The file is sent by the client as a remote external table
(REMOTESOURCE 'YES' of the IBM Data Server Driver of ibm_db), so no staging
table is needed. Prints "BEXHOMA_DELETED:<lineitems>:<orders>"; the exit code
is 0 on success, 1 on an error (the transaction is rolled back).

Environment: BEXHOMA_HOST, BEXHOMA_PORT, BEXHOMA_DATABASE, BEXHOMA_USER,
BEXHOMA_PASSWORD, BEXHOMA_SCHEMA (optional, else the default schema of the
user), DB2_DELIMITER (default '|').

Author: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
"""
import os
import sys

import ibm_db

from load import connect


def main():
    path = sys.argv[1]
    delimiter = os.environ.get('DB2_DELIMITER', '|')
    keys = ("SELECT orderkey FROM EXTERNAL '{file}' (orderkey BIGINT) "
            "USING (DELIMITER '{delim}' REMOTESOURCE 'YES' MAXERRORS 1)"
            .format(file=path, delim=delimiter))
    conn = None
    try:
        conn = connect()
        ibm_db.autocommit(conn, ibm_db.SQL_AUTOCOMMIT_OFF)
        stmt = ibm_db.exec_immediate(conn, 'DELETE FROM lineitem WHERE l_orderkey IN ({})'.format(keys))
        lineitems = ibm_db.num_rows(stmt)
        stmt = ibm_db.exec_immediate(conn, 'DELETE FROM orders WHERE o_orderkey IN ({})'.format(keys))
        orders = ibm_db.num_rows(stmt)
        ibm_db.commit(conn)
        print('BEXHOMA_DELETED:{}:{}'.format(lineitems, orders), flush=True)
        ibm_db.close(conn)
        sys.exit(0)
    except Exception as e:
        print('ERROR: {}'.format(e), flush=True)
        if conn is not None:
            try:
                ibm_db.rollback(conn)
                ibm_db.close(conn)
            except Exception:
                pass
        sys.exit(1)


if __name__ == '__main__':
    main()
