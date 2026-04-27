"""
Module that calculates the number of hunks made to a commit file.
"""
from statistics import median

from pydriller import ModificationType
from pydriller.metrics.process.process_metric import ProcessMetric


class HunksCount(ProcessMetric):
    """
    This class is responsible to implement the Number of Hunks metric for a
    file. As a hunk is a continuous block of changes in a diff, this number
    assesses how fragmented the commit file is (i.e. lots of changes all
    over the file versus one big change).

    If multiple commits are passed, it returns the median number of hunks in
    that range.
    """

    def count(self):
        """
        Return the number of hunks for each modified file.

        :return: int number of hunks
        """
        pass
