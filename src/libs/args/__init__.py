__all__ = ['ArgumentDefaultsHelpFormatter', 'ArgumentParserBody', 'arg_parser']

import argparse
import gettext
from argparse import HelpFormatter, Action, SUPPRESS, OPTIONAL, ZERO_OR_MORE, ArgumentParser
from typing import Optional, Any, Sequence, Type

from .. import TEXTDOMAINDIR

gettext.bindtextdomain('argparse', TEXTDOMAINDIR)


def __gettext(message: str) -> str:
    return gettext.dgettext('argparse', message)


def __ngettext(msgid1: str, msgid2: str, n: int) -> str:
    return gettext.dngettext('argparse', msgid1, msgid2, n)


argparse._ = __gettext
argparse.ngettext = __ngettext


class ArgumentDefaultsHelpFormatter(HelpFormatter):
    DEFAULTING_NARGS = (OPTIONAL, ZERO_OR_MORE)

    def _get_help_string(self, action: Action) -> Optional[str]:
        help_ = action.help
        if help_ is not None and '%(default)' not in action.help and action.default is not SUPPRESS:
            if action.option_strings or action.nargs in self.DEFAULTING_NARGS:
                help_ += ' (' + gettext.dgettext('argparse', 'default: {}').format('%(default)s') + ')'
        return help_


class ArgumentParserBody(ArgumentParser):
    def __init__(self,
                 prog: Optional[str] = None,
                 usage: Optional[str] = None,
                 description: Optional[str] = None,
                 epilog: Optional[str] = None,
                 parents: Sequence[ArgumentParser] = None,
                 formatter_class: Type[HelpFormatter] = ArgumentDefaultsHelpFormatter,
                 prefix_chars: str = '-',
                 fromfile_prefix_chars: Optional[str] = None,
                 argument_default: Any = None,
                 conflict_handler: str = 'error',
                 add_help: bool = True,
                 allow_abbrev: bool = True,
                 exit_on_error: bool = True):
        if parents is None:
            parents = []

        super().__init__(prog,
                         usage,
                         description,
                         epilog,
                         parents,
                         formatter_class,
                         prefix_chars,
                         fromfile_prefix_chars,
                         argument_default,
                         conflict_handler,
                         add_help,
                         allow_abbrev,
                         exit_on_error)

    def add_parent(self, parent: ArgumentParser):
        self._add_container_actions(parent)
        try:
            # noinspection PyProtectedMember
            defaults = parent._defaults
        except AttributeError:
            return
        self._defaults.update(defaults)


arg_parser = ArgumentParserBody()
