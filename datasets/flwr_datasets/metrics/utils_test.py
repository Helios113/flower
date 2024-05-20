# Copyright 2024 Flower Labs GmbH. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Tests for metrics utils."""

import unittest
from parameterized import parameterized
import pandas as pd
from flwr_datasets.metrics.utils import compute_counts, compute_distribution


class TestMetricsUtils(unittest.TestCase):

    @parameterized.expand([
        ([1, 2, 2, 3], [1, 2, 3, 4], pd.Series([1, 2, 1, 0], index=[1, 2, 3, 4])),
        ([], [1, 2, 3], pd.Series([0, 0, 0], index=[1, 2, 3])),
        ([1, 1, 2], [1, 2, 3, 4], pd.Series([2, 1, 0, 0], index=[1, 2, 3, 4])),
    ])
    def test_compute_counts(self, labels, unique_labels, expected):
        result = compute_counts(labels, unique_labels)
        pd.testing.assert_series_equal(result, expected)

    @parameterized.expand([
        ([1, 1, 2, 2, 2, 3], [1, 2, 3, 4],
         pd.Series([0.3333, 0.5, 0.1667, 0.0], index=[1, 2, 3, 4])),
        ([], [1, 2, 3], pd.Series([0.0, 0.0, 0.0], index=[1, 2, 3])),
        (['a', 'b', 'b', 'c'], ['a', 'b', 'c', 'd'],
         pd.Series([0.25, 0.50, 0.25, 0.0], index=['a', 'b', 'c', 'd'])),
    ])
    def test_compute_distribution(self, labels, unique_labels, expected):
        result = compute_distribution(labels, unique_labels)
        pd.testing.assert_series_equal(result, expected, atol=0.001)

    @parameterized.expand([
        (['a', 'b', 'b', 'c'], ['a', 'b', 'c']),
        ([1, 2, 2, 3, 3, 3, 4], [1, 2, 3, 4]),
    ])
    def test_distribution_sum_to_one(self, labels, unique_labels):
        result = compute_distribution(labels, unique_labels)
        self.assertAlmostEqual(result.sum(), 1.0)


if __name__ == '__main__':
    unittest.main()