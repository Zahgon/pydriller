import subprocess
from abc import ABC, abstractmethod
from pydriller.domain.developer import Developer
from typing import Optional, Tuple


class DeveloperFactory(ABC):

    @abstractmethod
    def get_developer(self, name: Optional[str] = None, email: Optional[str] = None) -> Developer:
        pass


class DefaultDeveloperFactory(DeveloperFactory):

    def get_developer(self, name: Optional[str] = None, email: Optional[str] = None) -> Developer:
        pass


class MailmapDeveloperFactory(DeveloperFactory):

    def __init__(self, conf):
        self.check_mailmap_cache = {}
        self._conf = conf

    def _run_check_mailmap(self, name: Optional[str] = None, email: Optional[str] = None) -> Tuple[str, str]:
        """ Call `git check-mailmap` to map names and emails of `Developer`s to canonical values.

        This method wraps a call to the `git-check-mailmap` binary. Given a name and email address of an author or
        committer, e.g., in the form `"My Name" "<me@work.com>"` it displays canonical names and email addresses based
        on entries provided in a repositories `.mailmap` file.
        The tool is documented here: https://git-scm.com/docs/git-check-mailmap/2.31.0

        In case anything goes wrong while calling `git-check-mailmap` the method returns the input values for name and
        email. This is inline with the behavior of `git-check-mailmap`, see documentation.
        """
        pass

    def get_developer(self, name: Optional[str] = None, email: Optional[str] = None) -> Developer:
        """ Get canonical names and emails for a `Developer`.

        If for a `Developer` name and email where never mapped to canonical values by calling the `git-check-mailmap`
        binary, then call the binary and cache the respective results in a dictionary to speed up later look ups.
        Otherwise, receive canonical name and email values directly from the cache.

        Caching results in a dictionary uses some RAM but I believe there are no repositories with so many authors that
        this will pose an issue on modern computers.
        """
        pass
