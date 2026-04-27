"""
Module that calculates the experience of contributors of a file.
"""
from pydriller import ModificationType
from pydriller.metrics.process.process_metric import ProcessMetric


class ContributorsExperience(ProcessMetric):
    """
    This class is responsible to implement the metric to measure the
    percentage of the lines authored by the highest contributor of a
    file in the provided evolution period [from_commit, to_commit].
    """

    def count(self):
        """
        Return the percentage of the lines authored by the highest contributor
        of a file for each modified file in the repository in the provided
        time range [from_commit, to_commit]

        :return: dict { filepath: float }
        of number of contributors for each modified file
        """
        pass
