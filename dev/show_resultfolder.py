"""
:Date: 2024-02-16
:Version: 1.0
:Authors: Patrick K. Erdelt

Show infos about results of bexhoma.
"""
import argparse
from dbmsbenchmarker import *
from prettytable import PrettyTable, ALL

if __name__ == '__main__':
    description = """Show infos about results of bexhoma."""
    # argparse
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-r', '--resultfolder', help='result folder of bexhoma', default='./')
    # evaluate args
    args = parser.parse_args()

    # path of folder containing experiment results
    resultfolder = args.resultfolder# "/home/perdelt/benchmarks/"

    # create evaluation object for result folder
    evaluate = inspector.inspector(resultfolder)

    # dataframe of experiments
    df = evaluate.get_experiments_preview().sort_values('time')
    df = df.reset_index()
    df['info'] = df['info'].str.replace('. ', '.\n')

    # Create a PrettyTable object
    pt = PrettyTable()
    pt.field_names = df.columns
    pt.align['info'] = 'r'  # 'r' for right alignment
    pt.hrules=ALL


    # Add rows to the PrettyTable
    for _, row in df.iterrows():
        pt.add_row(row)

    # Display the PrettyTable
    print(pt)
