# from .saver import FileSaver, ArchiverSaver
from .mediator import SavingMediator
from .files import (
    JSONFormatter,
    CSVFormatter,
    XLSXFormatter
)
from .archivers import ZIPArchiver
# from .layer import BaseFao

from enum import Enum


_Super_Worker_Saving_File_Key = "main_save_file"
_Sub_Worker_Saving_File_Key = "child_save_file"
_Activate_Compress_Key = "compress"


class SavingStrategy(Enum):

    ONE_THREAD_ONE_FILE = {
        _Super_Worker_Saving_File_Key: False,
        _Sub_Worker_Saving_File_Key: True,
        _Activate_Compress_Key: False
    }

    ALL_THREADS_ONE_FILE = {
        _Super_Worker_Saving_File_Key: True,
        _Sub_Worker_Saving_File_Key: False,
        _Activate_Compress_Key: False
    }

    ONE_THREAD_ONE_FILE_AND_COMPRESS_ALL = {
        _Super_Worker_Saving_File_Key: True,
        _Sub_Worker_Saving_File_Key: True,
        _Activate_Compress_Key: True
    }



class FileFormat(Enum):

    CSV = {
        "package": ".persistence.file",
        "formatter": "CSVFormatter"
    }

    XLSX = {
        "package": ".persistence.file",
        "formatter": "XLSXFormatter"
    }

    JSON = {
        "package": ".persistence.file",
        "formatter": "JSONFormatter"
    }

