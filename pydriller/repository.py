# Copyright 2018 Davide Spadini
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This module includes 1 class, Repository, main class of PyDriller.
"""

import logging
import math
import os
import shutil
import tempfile
import concurrent.futures
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import List, Generator, Optional, Union

from git import Repo

from pydriller.domain.commit import Commit
from pydriller.git import Git
from pydriller.utils.conf import Conf

logger = logging.getLogger(__name__)


class Repository:
    """
    This is the main class of PyDriller, responsible for running the study.
    """

    def __init__(self, path_to_repo: Union[str, List[str]],
                 single: Optional[str] = None,
                 since: Optional[datetime] = None, since_as_filter: Optional[datetime] = None, to: Optional[datetime] = None,
                 from_commit: Optional[str] = None, to_commit: Optional[str] = None,
                 from_tag: Optional[str] = None, to_tag: Optional[str] = None,
                 include_refs: bool = False,
                 include_remotes: bool = False,
                 num_workers: int = 1,
                 only_in_branch: Optional[str] = None,
                 only_modifications_with_file_types: Optional[List[str]] = None,
                 only_no_merge: bool = False,
                 only_authors: Optional[List[str]] = None,
                 only_commits: Optional[List[str]] = None,
                 only_releases: bool = False,
                 filepath: Optional[str] = None,
                 include_deleted_files: bool = False,
                 histogram_diff: bool = False,
                 skip_whitespaces: bool = False,
                 clone_repo_to: Optional[str] = None,
                 order: Optional[str] = None,
                 use_mailmap: bool = False):
        """
        Init a repository. The only required parameter is
        "path_to_repo": to analyze a single repo, pass the absolute path to
        the repo; if you need to analyze more repos, pass a list of absolute
        paths.

        Furthermore, PyDriller supports local and remote repositories: if
        you pass a path to a repo, PyDriller will run the study on that
        repo; if you pass an URL, PyDriller will clone the repo in a
        temporary folder, run the study, and delete the temporary folder.

        :param Union[str,List[str]] path_to_repo: absolute path (or list of
            absolute paths) to the repository(ies) to analyze
        :param str single: hash of a single commit to analyze
        :param datetime since: starting date
        :param datetime since_as_filter: starting date (scans all commits, does not stop at first commit with date < since_as_filter)
        :param datetime to: ending date
        :param str from_commit: starting commit (only if `since` is None)
        :param str to_commit: ending commit (only if `to` is None)
        :param str from_tag: starting the analysis from specified tag (only
            if `since` and `from_commit` are None)
        :param str to_tag: ending the analysis from specified tag (only if
            `to` and `to_commit` are None)
        :param bool include_refs: whether to include refs and HEAD in commit analysis
        :param bool include_remotes: whether to include remote commits in analysis
        :param int num_workers: number of workers (i.e., threads). Please note, if num_workers > 1 the commits order is not maintained.
        :param str only_in_branch: only commits in this branch will be analyzed
        :param List[str] only_modifications_with_file_types: only
            modifications with that file types will be analyzed
        :param bool only_no_merge: if True, merges will not be analyzed
        :param List[str] only_authors: only commits of these authors will be
            analyzed (the check is done on the username, NOT the email)
        :param List[str] only_commits: only these commits will be analyzed
        :param bool only_releases: analyze only tagged commits
        :param bool histogram_diff: add the "--histogram" option when asking for the diff
        :param bool skip_whitespaces: add the "-w" option when asking for the diff
        :param str clone_repo_to: if the repo under analysis is remote, clone the repo to the specified directory
        :param str filepath: only commits that modified this file will be analyzed
        :param bool include_deleted_files: include commits modifying a deleted file (useful when analyzing a deleted `filepath`)
        :param str order: order of commits. It can be one of: 'date-order',
            'author-date-order', 'topo-order', or 'reverse'. If order=None, PyDriller returns the commits from the oldest to the newest.
        :param bool use_mailmap: Map names and emails of authors and committers to canonical values when a .mailmap file is present in
            the repository.
        """
        file_modification_set = (
            None if only_modifications_with_file_types is None
            else set(only_modifications_with_file_types)
            )
        commit_set = (
            None if only_commits is None
            else set(only_commits)
            )

        options = {
            "git": None,
            "path_to_repo": path_to_repo,
            "from_commit": from_commit,
            "to_commit": to_commit,
            "from_tag": from_tag,
            "to_tag": to_tag,
            "since": since,
            "since_as_filter": since_as_filter,
            "to": to,
            "single": single,
            "include_refs": include_refs,
            "include_remotes": include_remotes,
            "num_workers": num_workers,
            "only_in_branch": only_in_branch,
            "only_modifications_with_file_types": file_modification_set,
            "only_no_merge": only_no_merge,
            "only_authors": only_authors,
            "only_commits": commit_set,
            "only_releases": only_releases,
            "skip_whitespaces": skip_whitespaces,
            "filepath": filepath,
            "include_deleted_files": include_deleted_files,
            "filepath_commits": None,
            "tagged_commits": None,
            "histogram": histogram_diff,
            "clone_repo_to": clone_repo_to,
            "order": order,
            "use_mailmap": use_mailmap
        }
        self._conf = Conf(options)

        # If the user provides a directory where to clone the repositories,
        # make sure we do not delete the directory after the study completes
        self._cleanup = False if clone_repo_to is not None else True

    @staticmethod
    def _is_remote(repo: str) -> bool:
        pass

    def _clone_remote_repo(self, tmp_folder: str, repo: str) -> str:
        pass

    def _clone_folder(self) -> str:
        pass

    @contextmanager
    def _prep_repo(self, path_repo: str) -> Generator[Git, None, None]:
        pass

    def traverse_commits(self) -> Generator[Commit, None, None]:
        """
        Analyze all the specified commits (all of them by default), returning
        a generator of commits.
        """
        pass

    def _iter_commits(self, commit: Commit) -> Generator[Commit, None, None]:
        pass

    @staticmethod
    def _split_in_chunks(full_list: List[Commit], num_workers: int) -> List[List[Commit]]:
        """
        Given the list of commits return chunks of commits based on the number of workers.

        :param List[Commit] full_list: full list of commits
        :param int num_workers: number of workers (i.e., threads)
        :return: Chunks of commits
        """
        pass

    @staticmethod
    def _get_repo_name_from_url(url: str) -> str:
        pass


class MalformedUrl(Exception):
    def __init__(self, message):
        super().__init__(message)
