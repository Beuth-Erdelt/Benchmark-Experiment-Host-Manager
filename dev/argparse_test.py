import argparse

if __name__ == '__main__':
    description = """Perform YCSB benchmarks in a Kubernetes cluster.
    Number of rows and operations is SF*1,000,000.
    This installs a clean copy for each target and split of the driver.
    Optionally monitoring is activated.
    """
    # argparse
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-dbms','--dbms', help='DBMS to load the data', choices=['PostgreSQL', 'MySQL', 'MariaDB', 'YugabyteDB', 'CockroachDB', 'DatabaseService', 'PGBouncer'], default=[], nargs='*')
    args = parser.parse_args()
    print(args)
    print(args.dbms)

