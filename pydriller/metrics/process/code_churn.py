"""
Module that calculates the number of hunks made to a commit file.
"""
import statistics
from typing import Optional, Dict, Tuple

from pydriller import ModificationType
from pydriller.metrics.process.process_metric import ProcessMetric


class CodeChurn(ProcessMetric):
    """
    This class is responsible to implement the Code Churn metric for a file.
    Depending on the parametrization of this class, a code churn is the sum of either
    (added lines - removed lines) or
    (added lines + removed lines)
    across the analyzed commits. It allows to count for the:
    * total number of code churns - count();
    * maximum code churn for all commits - max();
    * average code churn per commit.
    """

    def __init__(self, path_to_repo: str,
                 since=None,
                 to=None,
                 from_commit: Optional[str] = None,
                 to_commit: Optional[str] = None,
                 ignore_added_files=False,
                 add_deleted_lines_to_churn=False):
        """
        :ignore_added_files: if True, do not count churns for files when created
        :add_deleted_lines_to_churn: if True, also add deleted lines to churn calculation
        """

        super().__init__(path_to_repo, since=since, to=to, from_commit=from_commit, to_commit=to_commit)
        self.ignore_added_files = ignore_added_files
        self.add_deleted_lines_to_churn = add_deleted_lines_to_churn
        self.added_removed_lines: Dict[str, Tuple[int, int]] = {}
        self._initialize()

    def _initialize(self):
        pass

    def get_added_and_removed_lines(self) -> Dict[str, Tuple[int, int]]:
        """
        Returns a dictionary with file paths as keys and a tuple of added and removed lines as values.

        :return: A dictionary where the key is the file path, and the value is a tuple (added_lines, removed_lines).
        """
        pass

    def count(self):
        """
        Return the total number of code churns for each modified file.

        :return: int number of churns
        """
        pass

    def max(self):
        """
        Return the maximum code churn for each modified file.

        :return: int max number of churns
        """
        pass

    def avg(self):
        """
        Return the average number of code churns for each modified file.

        :return: int avg number of churns rounded off to the nearest integer
        """
        pass
