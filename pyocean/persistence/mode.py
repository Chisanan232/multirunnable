from .database.connection import BaseConnection
from .database.single_connection import SingleConnection
from .database.multi_connections import MultiConnections
from .file.saver import SingleFileSaver, MultiFileSaver
from .file.formatter import BaseFileFormatter, JSONFormatter, CSVFormatter, ExcelFormatter

from enum import Enum



class PersistenceMode(Enum):

    """
    Description:
        Appointed the persistence method and saving-process strategy.
        It has some strategy below:
          1. Database
             1-1. Single connection
             1-2. Multiple connections (Connection Pool)

          2. File
             2-1. Builder
                2-1-1.  SingleFileSaver
                2-1-2.  MultiFileSaver

             2-2. File Format
                2-2-1. JSON
                2-2-2. CSV
                2-2-3. Excel
                2-2-4. YAML
    """

    DATABASE_MODE = "database"
    FILE_MODE = "file"



class DatabaseMode(Enum):

    # By the class object
    # SINGLE_CONNECTION = SingleConnection()
    # MULTI_CONNECTIONS = MultiConnections()

    # By the class object
    SINGLE_CONNECTION = "SingleConnection"
    MULTI_CONNECTIONS = "MultiConnections"



class FileMode(Enum):

    SINGLE_JSON_STRATEGY = SingleFileSaver(file_path="/Users/bryantliu/Downloads/test.json", file_format=JSONFormatter())
    SINGLE_CSV_STRATEGY = SingleFileSaver(file_path="/Users/bryantliu/Downloads/test.csv", file_format=CSVFormatter())
    SINGLE_EXCEL_STRATEGY = SingleFileSaver(file_path="/Users/bryantliu/Downloads/test.xlsx", file_format=ExcelFormatter())

    MULTIPLE_JSON_STRATEGY = MultiFileSaver(file_path="/Users/bryantliu/Downloads/test.json", file_format=JSONFormatter())
    MULTIPLE_CSV_STRATEGY = MultiFileSaver(file_path="/Users/bryantliu/Downloads/test.csv", file_format=CSVFormatter())
    MULTIPLE_EXCEL_STRATEGY = MultiFileSaver(file_path="/Users/bryantliu/Downloads/test.xlsx", file_format=ExcelFormatter())

