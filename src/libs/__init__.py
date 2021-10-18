import gettext
import os
import pathlib
import sys

IS_UTIL = pathlib.Path(sys.argv[0]).parent.joinpath('src').is_dir()  # todo: Переделать определение точнее.
SRC_DIR = pathlib.Path(__file__).parent.parent  # todo: Изменить на нужный относительный путь.
DOMAIN = SRC_DIR.name
CURRENT_DIR = SRC_DIR.parent if IS_UTIL else SRC_DIR
DIR_PO = CURRENT_DIR.joinpath('po')
if not DIR_PO.is_dir():
    DIR_PO = None
TEXTDOMAINDIR = os.environ.get('TEXTDOMAINDIR')
if TEXTDOMAINDIR is None:
    TEXTDOMAINDIR = SRC_DIR.joinpath('locale')
    if not DIR_PO and not CURRENT_DIR.joinpath('locale').is_dir():
        # noinspection PyUnresolvedReferences,PyProtectedMember
        TEXTDOMAINDIR = gettext._default_localedir
TEXTDOMAINDIR = pathlib.Path(TEXTDOMAINDIR)

gettext.bindtextdomain(DOMAIN, str(TEXTDOMAINDIR))
gettext.textdomain(DOMAIN)
