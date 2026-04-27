"""
Module that calculates the History Complexity Period Factor (HCPF) \
for the History Complexity Metric (HCM).

The History Complexity Metric can be calculated by calling the \
method count as many times as the evolution period to analyze and \
summing up the results.

E.g.

hcpf_1 = HistoryComplexity(..., from_commit=c1, to_commit=c2).count()
hcpf_2 = HistoryComplexity(..., from_commit=c3, to_commit=c4).count()

hcm = hcpf_1 + hcpf_2

See https://ieeexplore.ieee.org/document/5070510
"""

from math import log

from pydriller import ModificationType
from pydriller.metrics.process.process_metric import ProcessMetric


class HistoryComplexity(ProcessMetric):
    """
    This class is responsible to implement the History Complexity Metric. \
    The metric assigns to each modified file the effect of the change \
    complexity of an evolution period.
    """

    def count(self):
        """
        Calculate the History Complexity Period Factor for each modified file \
        in the provided period [from_commit, to_commit], returning the \
        probability of each file being modified during that period

        :return: dict
        {
            filepath: float
        }
        """
        pass
