"""
Module that calculates the number of developers that contributed to each
modified file in the repo in a given time range.

See https://dl.acm.org/doi/10.1145/2025113.2025119
"""
from typing import Optional
from pydriller import ModificationType
from pydriller.metrics.process.process_metric import ProcessMetric


class ContributorsCount(ProcessMetric):
    """
    This class is responsible to implement the following metrics:

    * Contributors Count: measures the number of contributors who modified a
      file.

    * Minor Contributors Count: measures the number of contributors who
      authored less than 5% of code of a file.
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
        Return the number of contributors who modified a file.
        """
        pass

    def count_minor(self):
        """
        Return the number of contributors that authored less than
        5% of code of a file.
        """
        pass
