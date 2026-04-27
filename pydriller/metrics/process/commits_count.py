"""
Module that calculates the number of commits made to a file.
"""

from pydriller import ModificationType
from pydriller.metrics.process.process_metric import ProcessMetric


class CommitsCount(ProcessMetric):
    """
    This class is responsible to implement the Commit Count metric to \
    measure the number of commits made to a file
    """

    def count(self):
        pass
