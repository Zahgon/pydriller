"""
Configuration module.
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union

import pytz
from gitdb.exc import BadName

from pydriller.domain.commit import Commit
from pydriller.utils.mailmap import DefaultDeveloperFactory, MailmapDeveloperFactory

logger = logging.getLogger(__name__)


class Conf:
    """
    Configuration class. This class holds all the possible configurations of
    the mining process (i.e., starting and ending dates, branches, etc.)
    It's also responsible for checking whether the filters are correct (i.e.,
    the user did not specify 2 starting commits).
    """

    def __init__(self, options: Dict[str, Any]) -> None:
        # insert all the configurations in a local dictionary
        self._options = {}
        for key, val in options.items():
            self._options[key] = val

        self._sanity_check_repos(self.get('path_to_repo'))
        if isinstance(self.get('path_to_repo'), str):
            self.set_value('path_to_repos', [self.get('path_to_repo')])
        else:
            self.set_value('path_to_repos', self.get('path_to_repo'))

        if self._options.get("use_mailmap"):
            self.set_value("developer_factory", MailmapDeveloperFactory(self))
        else:
            self.set_value("developer_factory", DefaultDeveloperFactory())

    def set_value(self, key: str, value: Any) -> None:
        """
        Save the value of a configuration.

        :param key: configuration (i.e., start date)
        :param value: value
        """
        pass

    def get(self, key: str) -> Any:
        """
        Return the value of the configuration.

        :param key: configuration name
        :return: value of the configuration, None if not present
        """
        pass

    @staticmethod
    def _sanity_check_repos(path_to_repo: Union[str, List[str]]) -> None:
        """
        Checks if repo is of type str or list.

        @param path_to_repo: path to the repo as provided by the user.
        @return:
        """
        pass

    def _check_only_one_from_commit(self) -> None:
        pass

    def _check_only_one_to_commit(self) -> None:
        pass

    def sanity_check_filters(self) -> None:
        """
        Check if the values passed by the user are correct.

        """
        pass

    def _check_correct_filters_order(self) -> None:
        """
        Check that from_commit comes before to_commit
        """
        pass

    def _swap_commit_fiters(self) -> None:
        # reverse from and to commit
        pass

    @staticmethod
    def _is_commit_before(commit_before: Commit, commit_after: Commit) -> bool:
        pass

    def get_starting_commit(self) -> Optional[List[str]]:
        """
        Get the starting commit from the 'from_commit' or 'from_tag'
        filter.
        """
        pass

    def get_ending_commit(self) -> Optional[str]:
        """
        Get the ending commit from the 'to', 'to_commit' or 'to_tag' filter.
        """
        pass

    @staticmethod
    def only_one_filter(arr: List[Any]) -> bool:
        """
        Return true if in 'arr' there is at most 1 filter to True.

        :param arr: iterable object
        :return:
        """
        pass

    def build_args(self) -> Tuple[Union[str, List[str]], Dict[str, Any]]:
        """
        This function builds the argument for git rev-list.

        :return:
        """
        pass

    def is_commit_filtered(self, commit: Commit):
        # pylint: disable=too-many-branches,too-many-return-statements
        """
        Check if commit has to be filtered according to the filters provided
        by the user.

        :param Commit commit: Commit to check
        :return:
        """
        pass

    def _has_modification_with_file_type(self, commit: Commit) -> bool:
        pass

    def _check_timezones(self):
        pass

    @staticmethod
    def _replace_timezone(dt: datetime) -> datetime:
        pass
