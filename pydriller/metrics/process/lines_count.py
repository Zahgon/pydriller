"""
Module that calculates the number of normalized added and deleted lines of a
file.
"""
import statistics
from typing import Optional
from pydriller import ModificationType
from pydriller.metrics.process.process_metric import ProcessMetric


class LinesCount(ProcessMetric):
    """
    This class is responsible to implement the following metrics:

    * Changed Lines: the number of added and deleted lines in the evolution
        period [from_commit, to_commit]

    * Added Lines: the sum over all commits of the lines of code added to a
        file in the evolution period [from_commit, to_commit]

    * Max Added Lines: the maximum number of lines of code added to a file
        per commit in the evolution period [from_commit, to_commit]

    * Average Added Lines: the average lines of code added to a file per commit
        in the evolution period [from_commit, to_commit]

    * Removed Lines: the sum over all commits of the lines of code removed to a
        file in the evolution period [from_commit, to_commit]

    * Max Removed Lines: the maximum number of lines of code removed to a file
        per commit in the evolution period [from_commit, to_commit]

    * Average Removed Lines: the average lines of code removed to a file per
        commit in the evolution period [from_commit, to_commit]

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

    def count(self):
        """
        Sum over all commits of the lines of code added and removed to a file .

        :return: int lines added + lines removed
        """
        pass

    def count_added(self):
        """
        Sum over all commits of the lines of code added to a file .

        :return: int lines added
        """
        pass

    def max_added(self):
        """
        Maximum number of lines of code added to a file for all commits

        :return: int max number of lines added
        """
        pass

    def avg_added(self):
        """
        Average lines of code added to a file per commit

        :return: int avg number of lines rounded off to the nearest integer
        """
        pass

    def count_removed(self):
        """
        Sum over all commits of the lines of code removed to a file .

        :return: int lines removed
        """
        pass

    def max_removed(self):
        """
        Maximum number of lines of code removed in a file for all commits

        :return: int max number of lines removed
        """
        pass

    def avg_removed(self):
        """
        Average lines of code removed in a file per commit

        :return: int rounded off to the nearest integer
        """
        pass
