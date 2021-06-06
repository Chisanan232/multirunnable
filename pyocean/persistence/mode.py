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

    SINGLE_DATABASE_CONNECTION = ""
    MULTI_DATABASE_CONNECTION = ""

    SINGLE_FILE_IO = ""
    MULTI_FILE_IO = ""

