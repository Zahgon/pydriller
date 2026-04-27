"""
Module that calculates the number of files committed together.
"""
import statistics
from typing import Optional

from pydriller.metrics.process.process_metric import ProcessMetric


class ChangeSet(ProcessMetric):
    """
    This class is responsible to implement the Change Set metric that
    measures the

    * maximum number of files committed together - max();
    * average number of files committed together - avg().
    """

    def __init__(self, path_to_repo: str,
                 since=None,
                 to=None,
                 from_commit: Optional[str] = None,
                 to_commit: Optional[str] = None):

        super().__init__(path_to_repo, since=since, to=to, from_commit=from_commit, to_commit=to_commit)
        self._initialize()

    def _initialize(self):

        pass

    def max(self):
        """
        Return the maximum number of files committed together.

        :return: int max number of files committed together
        """
        pass

    def avg(self):
        """
        Return the average number of files committed together.

        :return: int avg number of files rounded off to the nearest integer
        """
        pass
