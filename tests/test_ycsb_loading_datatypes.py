"""YCSB loading results of a loader without a [CLEANUP] block (e.g. TiDB)."""
import unittest

import pandas as pd

from bexhoma.benchmarks.ycsb.evaluator import YcsbEvaluator


class LoadingSetDatatypesTest(unittest.TestCase):
    def test_missing_cleanup_columns_are_filled_with_zero(self):
        evaluator = YcsbEvaluator.__new__(YcsbEvaluator)
        df = pd.DataFrame([{
            'code': 1, 'connection': 'a', 'configuration': 'c', 'experiment_run': 1, 'client': 1,
            'pod': 'p', 'pod_count': 1, 'threads': 2, 'target': 0, 'SF': 1, 'workload': 'a',
            'operations': 10, 'errors': 0,
            '[OVERALL].RunTime(ms)': 5, '[OVERALL].Throughput(ops/sec)': 2.0,
            '[INSERT].Operations': 10, '[INSERT].AverageLatency(us)': 1.0,
            '[INSERT].MinLatency(us)': 1.0, '[INSERT].MaxLatency(us)': 1.0,
            '[INSERT].95thPercentileLatency(us)': 1.0, '[INSERT].99thPercentileLatency(us)': 1.0,
            '[INSERT].Return=OK': 10, 'phase': 'x',
        }])
        typed = evaluator.loading_set_datatypes(df)
        self.assertEqual(typed['[CLEANUP].Operations'].tolist(), [0])
        self.assertEqual(len(evaluator.loading_aggregate_by_parallel_pods(typed)), 1)


if __name__ == '__main__':
    unittest.main()
