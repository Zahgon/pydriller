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
This module contains all the classes regarding a specific commit, such as
Commit, Modification,
ModificationType and Method.
"""
import logging
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, List, Set, Dict, Tuple, Optional, Union

import hashlib

import lizard
import lizard_languages
from git import Diff, Git, NULL_TREE
from git.objects import Commit as GitCommit
from git.objects.base import IndexObject

from pydriller.domain.developer import Developer

logger = logging.getLogger(__name__)


class ModificationType(Enum):
    """
    Type of Modification. Can be ADD, COPY, RENAME, DELETE, MODIFY or UNKNOWN.
    """

    ADD = 1
    COPY = 2
    RENAME = 3
    DELETE = 4
    MODIFY = 5
    UNKNOWN = 6


class DMMProperty(Enum):
    """
    Maintainability properties of the Delta Maintainability Model.
    """

    UNIT_SIZE = 1
    UNIT_COMPLEXITY = 2
    UNIT_INTERFACING = 3


class Method:
    """
    This class represents a method in a class. Contains various information
    extracted through Lizard.
    """

    def __init__(self, func: Any) -> None:
        """
        Initialize a method object. This is calculated using Lizard: it parses
        the source code of all the modifications in a commit, extracting
        information of the methods contained in the file (if the file is a
        source code written in one of the supported programming languages).
        """

        self.name: str = func.name
        self.long_name: str = func.long_name
        self.filename: str = func.filename
        self.nloc: int = func.nloc
        self.complexity: int = func.cyclomatic_complexity
        self.token_count: int = func.token_count
        self.parameters: List[str] = func.parameters
        self.start_line: int = func.start_line
        self.end_line: int = func.end_line
        self.fan_in: int = func.fan_in
        self.fan_out: int = func.fan_out
        self.general_fan_out: int = func.general_fan_out
        self.length: int = func.length
        self.top_nesting_level: int = func.top_nesting_level

    def __eq__(self, other) -> bool:
        return self.name == other.name and self.parameters == other.parameters

    def __hash__(self) -> int:
        # parameters are used in hashing in order to
        # prevent collisions when overloading method names
        return hash(
            (
                "name",
                self.name,
                "long_name",
                self.long_name,
                "params",
                tuple(x for x in self.parameters),
            )
        )

    UNIT_SIZE_LOW_RISK_THRESHOLD = 15
    """
    Threshold used in the Delta Maintainability Model to establish whether a method
    is low risk in terms of its size.
    The procedure to obtain the threshold is described in the
    :ref:`PyDriller documentation <Properties>`.
    """

    UNIT_COMPLEXITY_LOW_RISK_THRESHOLD = 5
    """
    Threshold used in the Delta Maintainability Model to establish whether a method
    is low risk in terms of its cyclomatic complexity.
    The procedure to obtain the threshold is described in the
    :ref:`PyDriller documentation <Properties>`.
    """

    UNIT_INTERFACING_LOW_RISK_THRESHOLD = 2
    """
    Threshold used in the Delta Maintainability Model to establish whether a method
    is low risk in terms of its interface.
    The procedure to obtain the threshold is described in the
    :ref:`PyDriller documentation <Properties>`.
    """

    def is_low_risk(self, dmm_prop: DMMProperty) -> bool:
        """
        Predicate indicating whether this method is low risk in terms of
        the given property.

        :param dmm_prop: Property according to which this method is considered risky.
        :return: True if and only if the method is considered low-risk w.r.t. this property.
        """
        pass


class ModifiedFile:
    """
    This class contains information regarding a modified file in a commit.
    """

    def __init__(
            self,
            diff: Diff,
    ):
        """
        Initialize a modified file. A modified file carries on information
        regarding the changed file. Normally, you shouldn't initialize a new
        one.
        """
        self._c_diff = diff

        self._nloc = None
        self._complexity = None
        self._token_count = None
        self._function_list: List[Method] = []
        self._function_list_before: List[Method] = []

    def __hash__(self) -> int:
        """
        Implements hashing similar as Git would do it. Alternatively, if the
        object had the hash of th Git Blob, one could use that directly.

        :return: int hash
        """
        string = f"{self.change_type.name} {self.new_path} {self.content!r}"
        return hash(hashlib.sha256(string.encode("utf-8")).hexdigest())

    @property
    def change_type(self) -> ModificationType:
        pass

    @staticmethod
    def _from_change_to_modification_type(diff: Diff) -> ModificationType:
        pass

    @property
    def diff(self) -> str:
        pass

    def _get_decoded_str(self, diff: Union[str, bytes, None]) -> Optional[str]:
        pass

    @property
    def content(self) -> Optional[bytes]:
        pass

    @property
    def content_before(self) -> Optional[bytes]:
        pass

    def _get_undecoded_content(self, blob: Optional[IndexObject]) -> Optional[bytes]:
        pass

    @property
    def source_code(self) -> Optional[str]:
        pass

    @property
    def source_code_before(self) -> Optional[str]:
        pass

    @property
    def added_lines(self) -> int:
        """
        Return the total number of added lines in the file.

        :return: int lines_added
        """
        pass

    @property
    def deleted_lines(self) -> int:
        """
        Return the total number of deleted lines in the file.

        :return: int lines_deleted
        """
        pass

    @property
    def old_path(self) -> Optional[str]:
        """
        Old path of the file. Can be None if the file is added.

        :return: str old_path
        """
        pass

    @property
    def new_path(self) -> Optional[str]:
        """
        New path of the file. Can be None if the file is deleted.

        :return: str new_path
        """
        pass

    @property
    def filename(self) -> str:
        """
        Return the filename. Given a path-like-string (e.g.
        "/Users/dspadini/pydriller/myfile.py") returns only the filename
        (e.g. "myfile.py")

        :return: str filename
        """
        pass

    @property
    def language_supported(self) -> bool:
        """
        Return whether the language used in the modification can be analyzed by Pydriller.
        Languages are derived from the file  extension.
        Supported languages are those supported by Lizard.

        :return: True iff language of this Modification can be analyzed.
        """
        pass

    @property
    def nloc(self) -> Optional[int]:
        """
        Calculate the LOC of the file.

        :return: LOC of the file
        """
        pass

    @property
    def complexity(self) -> Optional[int]:
        """
        Calculate the Cyclomatic Complexity of the file.

        :return: Cyclomatic Complexity of the file
        """
        pass

    @property
    def token_count(self) -> Optional[int]:
        """
        Calculate the token count of functions.

        :return: token count
        """
        pass

    @property
    def diff_parsed(self) -> Dict[str, List[Tuple[int, str]]]:
        """
        Returns a dictionary with the added and deleted lines.
        The dictionary has 2 keys: "added" and "deleted", each containing the
        corresponding added or deleted lines. For both keys, the value is a
        list of Tuple (int, str), corresponding to (number of line in the file,
        actual line).

        :return: Dictionary
        """
        pass

    @staticmethod
    def _get_line_numbers(line: str) -> Tuple[int, int]:
        pass

    @property
    def methods(self) -> List[Method]:
        """
        Return the list of methods in the file. Every method
        contains various information like complexity, loc, name,
        number of parameters, etc.

        :return: list of methods
        """
        pass

    @property
    def methods_before(self) -> List[Method]:
        """
        Return the list of methods in the file before the
        change happened. Each method will have all specific
        info, e.g. complexity, loc, name, etc.

        :return: list of methods
        """
        pass

    @property
    def changed_methods(self) -> List[Method]:
        """
        Return the list of methods that were changed. This analysis
        is more complex because Lizard runs twice: for methods before
        and after the change

        :return: list of methods
        """
        pass

    @staticmethod
    def _risk_profile(
            methods: List[Method], dmm_prop: DMMProperty
    ) -> Tuple[int, int]:
        """
        Return the risk profile of the set of methods, with two bins: risky, or non risky.
        The risk profile is a pair (v_low, v_high), where
        v_low is the volume of the low risk methods in the list, and
        v_high is the volume of the high risk methods in the list.

        :param methods: List of methods for which risk profile is to be determined
        :param dmm_prop: Property indicating the type of risk
        :return: total risk profile for methods according to property.
        """
        pass

    def _delta_risk_profile(self, dmm_prop: DMMProperty) -> Tuple[int, int]:
        """
        Return the delta risk profile of this commit, which a pair (dv1, dv2), where
        dv1 is the total change in volume (lines of code) of low risk methods, and
        dv2 is the total change in volume of the high risk methods.

        :param dmm_prop: Property indicating the type of risk
        :return: total delta risk profile for this property.
        """
        pass

    def _calculate_metrics(self, include_before: bool = False) -> None:
        """
        :param include_before: either to compute the metrics
        for source_code_before, i.e. before the change happened
        """
        pass

    def _get_decoded_content(self, content: bytes) -> Optional[str]:
        pass

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ModifiedFile):
            return NotImplemented
        if self is other:
            return True
        return self.__dict__ == other.__dict__


class Commit:
    """
    Class representing a Commit. Contains all the important information such
    as hash, author, dates, and modified files.
    """

    def __init__(self, commit: GitCommit, conf) -> None:
        """
        Create a commit object.

        :param commit: GitPython Commit object
        :param conf: Configuration class
        """
        self._c_object = commit
        self._conf = conf
        self._stats_cache = None

    def __hash__(self) -> int:
        """
        Since already used in Git for identification use the SHA of the commit
        as hash value.

        :return: int hash
        """
        # Unfortunately, the Git hash cannot be used for the Python object
        # directly. The documentation says it "should" return an integer
        # https://docs.python.org/3/reference/datamodel.html#object.__hash__
        # but I just learned it **has** to return one.
        return hash(self._c_object.hexsha)

    @property
    def hash(self) -> str:
        """
        Return the SHA of the commit.

        :return: str hash
        """
        pass

    @property
    def author(self) -> Developer:
        """
        Return the author of the commit as a Developer object.

        :return: author
        """
        pass

    @property
    def co_authors(self) -> List[Developer]:
        """
        Return the co-authors of the commit as a list of Developer objects.

        :return: List[Developer] author
        """
        pass

    @property
    def committer(self) -> Developer:
        """
        Return the committer of the commit as a Developer object.

        :return: committer
        """
        pass

    @property
    def project_name(self) -> str:
        """
        Return the project name.

        :return: project name
        """
        pass

    @property
    def project_path(self) -> str:
        """
        Return the absolute path of the project.

        :return: project path
        """
        pass

    @property
    def author_date(self) -> datetime:
        """
        Return the authored datetime.

        :return: datetime author_datetime
        """
        pass

    @property
    def committer_date(self) -> datetime:
        """
        Return the committed datetime.

        :return: datetime committer_datetime
        """
        pass

    @property
    def author_timezone(self) -> int:
        """
        Author timezone expressed in seconds from epoch.

        :return: int timezone
        """
        pass

    @property
    def committer_timezone(self) -> int:
        """
        Author timezone expressed in seconds from epoch.

        :return: int timezone
        """
        pass

    @property
    def msg(self) -> str:
        """
        Return commit message.

        :return: str commit_message
        """
        pass

    @property
    def parents(self) -> List[str]:
        """
        Return the list of parents SHAs.

        :return: List[str] parents
        """
        pass

    @property
    def merge(self) -> bool:
        """
        Return True if the commit is a merge, False otherwise.

        :return: bool merge
        """
        pass

    def _stats(self):
        pass

    def _list_from_string(self, text: str):
        pass

    @property
    def insertions(self) -> int:
        """
        Return the number of added lines in the commit (as shown from --shortstat).

        :return: int insertion lines
        """
        pass

    @property
    def deletions(self) -> int:
        """
        Return the number of deleted lines in the commit (as shown from --shortstat).

        :return: int deletion lines
        """
        pass

    @property
    def lines(self) -> int:
        """
        Return the number of modified lines in the commit (as shown from --shortstat).

        :return: int insertion + deletion lines
        """
        pass

    @property
    def files(self) -> int:
        """
        Return the number of modified files of the commit (as shown from --shortstat).

        :return: int modified files number
        """
        pass

    @property
    def modified_files(self) -> List[ModifiedFile]:
        """
        Return a list of modified files. The list is empty if the commit is
        a merge commit. For more info on this, see
        https://haacked.com/archive/2014/02/21/reviewing-merge-commits/ or
        https://github.com/ishepard/pydriller/issues/89#issuecomment-590243707

        :return: List[Modification] modifications
        """
        pass

    def _parse_diff(self, diff_index: List[Diff]) -> List[ModifiedFile]:
        pass

    @property
    def in_main_branch(self) -> bool:
        """
        Return True if the commit is in the main branch, False otherwise.

        :return: bool in_main_branch
        """
        pass

    @property
    def branches(self) -> Set[str]:
        """
        Return the set of branches that contain the commit.

        :return: set(str) branches
        """
        pass

    @property
    def dmm_unit_size(self) -> Optional[float]:
        """
        Return the Delta Maintainability Model (DMM) metric value for the unit size property.

        It represents the proportion (between 0.0 and 1.0) of maintainability improving
        change, when considering the lengths of the modified methods.

        It rewards (value close to 1.0) modifications to low-risk (small) methods,
        or spliting risky (large) ones.
        It penalizes (value close to 0.0) working on methods that remain large
        or get larger.

        :return: The DMM value (between 0.0 and 1.0) for method size in this commit,
                 or None if none of the programming languages in the commit are supported.
        """
        pass

    @property
    def dmm_unit_complexity(self) -> Optional[float]:
        """
        Return the Delta Maintainability Model (DMM) metric value for the unit complexity property.

        It represents the proportion (between 0.0 and 1.0) of maintainability improving
        change, when considering the cyclomatic complexity of the modified methods.

        It rewards (value close to 1.0) modifications to low-risk (low complexity) methods,
        or spliting risky (highly complex) ones.
        It penalizes (value close to 0.0) working on methods that remain complex
        or get more complex.

        :return: The DMM value (between 0.0 and 1.0) for method complexity in this commit.
                 or None if none of the programming languages in the commit are supported.
        """
        pass

    @property
    def dmm_unit_interfacing(self) -> Optional[float]:
        """
        Return the Delta Maintainability Model (DMM) metric value for the unit interfacing property.

        It represents the proportion (between 0.0 and 1.0) of maintainability improving
        change, when considering the interface (number of parameters) of the modified methods.

        It rewards (value close to 1.0) modifications to low-risk (with  few parameters) methods,
        or spliting risky (with many parameters) ones.
        It penalizes (value close to 0.0) working on methods that continue to have
        or are extended with too many parameters.

        :return: The dmm value (between 0.0 and 1.0) for method interfacing in this commit.
                  or None if none of the programming languages in the commit are supported.
        """
        pass

    def _delta_maintainability(self, dmm_prop: DMMProperty) -> Optional[float]:
        """
        Compute the Delta Maintainability Model (DMM) value for the given risk predicate.
        The DMM value is computed as the proportion of good change in the commit:
        Good changes: Adding low risk code or removing high risk codee.
        Bad changes: Adding high risk code or removing low risk code.

        :param dmm_prop: Property indicating the type of risk
        :return: dmm value (between 0.0 and 1.0) for the property represented in the property.
        """
        pass

    def _delta_risk_profile(
            self, dmm_prop: DMMProperty
    ) -> Optional[Tuple[int, int]]:
        """
        Return the delta risk profile of this commit, which a pair (dv1, dv2), where
        dv1 is the total change in volume (lines of code) of low risk methods, and
        dv2 is the total change in volume of the high risk methods.

        :param dmm_prop: Property indicating the type of risk
        :return: total delta risk profile for this commit.
        """
        pass

    @staticmethod
    def _good_change_proportion(
            low_risk_delta: int, high_risk_delta: int
    ) -> Optional[float]:
        """
        Given a delta risk profile, compute the proportion of "good" change in the total change.
        Increasing low risk code, or decreasing high risk code, is considered good.
        Other types of changes are considered not good.

        :return: proportion of good change in total change, or None if the total change is zero.
        """
        pass

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Commit):
            return NotImplemented
        if self is other:
            return True

        return self.__dict__ == other.__dict__
