from enum import Enum



class PersistenceMode(Enum):

    """
    Description:
        Appointed the persistence method and saving-process strategy.
        It has some strategy below:
          1. Database

          2. File
             2-1. General file like .csv, .json or something else.
             2-2. Archiver like .zip, .tar or something else.
    """

    DATABASE = {
        "properties_key": "database"
    }

    FILE = {
        "properties_key": "file"
    }

    ARCHIVER = {
        "properties_key": "archiver"
    }



class DatabaseDriver(Enum):

    MySQL = {
        "properties_key": "mysql"
    }
