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
This module includes 1 class, Git, representing a repository in Git.
"""

import logging
import os
from pathlib import Path
from typing import List, Dict, Optional, Set, Generator

from git import Repo, GitCommandError
from git.objects import Commit as GitCommit

from pydriller.domain.commit import Commit, ModificationType, ModifiedFile
from pydriller.utils.conf import Conf

logger = logging.getLogger(__name__)


class Git:
    """
    Class representing a repository in Git. It contains most of the logic of
    PyDriller: obtaining the list of commits, checkout, reset, etc.
    """

    def __init__(self, path: str, conf=None):
        """
        Init the Git Repository.

        :param str path: path to the repository
        """
        self.path = Path(path).expanduser().resolve()
        self.project_name = self.path.name
        self._repo = None

        # if no configuration is passed, then creates a new "emtpy" one
        # with just "path_to_repo" inside.
        if conf is None:
            conf = Conf({
                "path_to_repo": str(self.path),
                "git": self
            })

        self._conf = conf
        self._conf.set_value("main_branch", None)  # init main_branch to None

        # Initialize repository
        self._open_repository()

    @property
    def repo(self) -> Repo:
        """
        GitPython object Repo.

        :return: Repo
        """
        pass

    def clear(self):
        """
        According to GitPython's documentation, sometimes it leaks resources.
        This holds especially for Windows users. Hence, we need to clear the
        cache manually.
        """
        pass

    def _open_repository(self):
        pass

    def _discover_main_branch(self, repo):
        pass

    def get_head(self) -> Commit:
        """
        Get the head commit.

        :return: Commit of the head commit
        """
        pass

    def get_list_commits(self, rev='HEAD', **kwargs) -> Generator[Commit, None, None]:
        """
        Return a generator of commits of all the commits in the repo.

        :return: Generator[Commit], the generator of all the commits in the
            repo
        """
        pass

    def get_commit(self, commit_id: str) -> Commit:
        """
        Get the specified commit.

        :param str commit_id: hash of the commit to analyze
        :return: Commit
        """
        pass

    def get_commit_from_gitpython(self, commit: GitCommit) -> Commit:
        """
        Build a PyDriller commit object from a GitPython commit object.
        This is internal of PyDriller, I don't think users generally will need
        it.

        :param GitCommit commit: GitPython commit
        :return: Commit commit: PyDriller commit
        """
        pass

    def checkout(self, _hash: str) -> None:
        """
        Checkout the repo at the speficied commit.
        BE CAREFUL: this will change the state of the repo, hence it should
        *not* be used with more than 1 thread.

        :param _hash: commit hash to checkout
        """
        pass

    def files(self) -> List[str]:
        """
        Obtain the list of the files (excluding .git directory).

        :return: List[str], the list of the files
        """
        pass

    def reset(self) -> None:
        """
        Reset the state of the repo, checking out the main branch and
        discarding
        local changes (-f option).

        """
        pass

    def total_commits(self) -> int:
        """
        Calculate total number of commits.

        :return: the total number of commits
        """
        pass

    def get_commit_from_tag(self, tag: str) -> Commit:
        """
        Obtain the tagged commit.

        :param str tag: the tag
        :return: Commit commit: the commit the tag referred to
        """
        pass

    def get_tagged_commits(self):
        """
        Obtain the hash of all the tagged commits.

        :return: list of tagged commits (can be empty if there are no tags)
        """
        pass

    def get_commits_last_modified_lines(self, commit: Commit,
                                        modification: Optional[ModifiedFile] = None,
                                        hashes_to_ignore_path: Optional[str] = None) \
            -> Dict[str, Set[str]]:
        """
        Given the Commit object, returns the set of commits that last
        "touched" the lines that are modified in the files included in the
        commit. It applies SZZ.

        The algorithm works as follow: (for every file in the commit)

        1- obtain the diff

        2- obtain the list of deleted lines

        3- blame the file and obtain the commits were those lines were added

        Can also be passed as parameter a single Modification, in this case
        only this file will be analyzed.

        :param Commit commit: the commit to analyze
        :param Modification modification: single modification to analyze
        :param str hashes_to_ignore_path: path to a file containing hashes of
               commits to ignore.
        :return: Dict commits: a dictionary having as keys the files of the commit,
                 and as values the commits that last touched those files.
        """
        pass

    def diff(self, from_commit_id: str, to_commit_id: str) -> List[ModifiedFile]:
        pass

    def _calculate_last_commits(self, commit: Commit,
                                modifications: List[ModifiedFile],
                                hashes_to_ignore_path: Optional[str] = None) \
            -> Dict[str, Set[str]]:

        pass

    def _get_blame(self, commit_hash: str, path: str, hashes_to_ignore_path: Optional[str] = None):
        pass

    @staticmethod
    def _useless_line(line: str):
        # this covers comments in Java and Python, as well as empty lines.
        # More have to be added!
        pass

    def get_commits_modified_file(self, filepath: str, include_deleted_files=False) -> List[str]:
        """
        Given a filepath, returns all the commits that modified this file
        (following renames).

        :param str filepath: path to the file
        :param bool include_deleted_files: if True, include commits that modifies a deleted file
        :return: the list of commits' hash
        """
        pass

    def __del__(self):
        self.clear()
