===================
Persistence - File
===================

*module* multirunnable.persistence.file

The subpackage could persistence data as file format for *MultiRunnable*.
It could help you persistence data as file in running process with multiple runnable objects.

In parallelism, it has some different ways to save result:

* Every runnable objects save one file
* Every runnable objects return result back to main runnable object (like main thread or main process) and save it to one file
* Every runnable objects save one file and main runnable object compress them to a archiver type file.

So in *.persistence.file* subpackage, it has 5 sections:

* Saving Strategy
    *object* multirunnable.persistence.file.SavingStrategy

    Enums:

    * ONE_THREAD_ONE_FILE
    * ALL_THREADS_ONE_FILE
    * ONE_THREAD_ONE_FILE_AND_COMPRESS_ALL

* File Formatter
    *module* multirunnable.persistence.file.files

    Objects:

    * CSVFormatter
    * XLSXFormatter
    * JSONFormatter

* Archiver Formatter
    *module* multirunnable.persistence.file.archivers

    Objects:

    * ZIPArchiver

* Savers
    *module* multirunnable.persistence.file.saver

    Objects:

    * FileSaver
    * ArchiverSaver

* Mediators
    *module* multirunnable.persistence.file.mediator

    Objects:

    * SavingMediator

* Persistence Layer
    *module* multirunnable.persistence.file.layer

    Objects:

    * BaseFao


Saving Strategy Objects
========================

*object* multirunnable.persistence.file.SavingStrategy

Enums:

* ONE_THREAD_ONE_FILE
    Every runnable objects save one file

* ALL_THREADS_ONE_FILE
    Every runnable objects return result back to main runnable object (like main thread or main process) and save it to one file

* ONE_THREAD_ONE_FILE_AND_COMPRESS_ALL
    Every runnable objects save one file and main runnable object compress them to a archiver type file.


Files Objects
================

*module* multirunnable.persistence.file.files

This module responses of annotating all attributes and methods for different file format it should have.
It ONLY annotates attributes and methods (behaviors), so it won't tell you how to use it.
Currently, *MultiRunnable* provides 3 formats: *CSV*, *XLSX* and *JSON*.
They all extends from class *File* to implement their details.

File
--------------

*class* multirunnable.persistence.file.files.\ **File**\ *()*

    This is the basically class to let every subclass which for different file format to implement details and extend features.
    It already has 3 properties for subclass: *file_path*, *mode* and *encoding*.


*property* **file_path**\ *()*

    The target file path. It could use *getting* and *setting* of this property.


*property* **mode**\ *()*

    The mode how to operate with file. It could use *getting* and *setting* of this property.


*property* **encoding**\ *()*

    The encoding of file IO. It could use *getting* and *setting* of this property.


*abstract* **open**\ *()*

    Open an target file as an object which would be assign to class level variable. So it won't return anything.


*abstract* **write**\ *(data: List[list], io_wrapper=None)*

    Write the data into file IO object.


*abstract* **close**\ *()*

    Close the file IO. It MUST to do finally no matter you operate with file successfully or not.


*abstract* **stream**\ *(data: List[list])*

    Return a IO streaming (ex: io.StringIO) object which save the data content.


CSVFormatter
--------------

*class* multirunnable.persistence.file.files.\ **CSVFormatter**\ *()*

    The implementation for saving data as *CSV* format.


XLSXFormatter
---------------

*class* multirunnable.persistence.file.files.\ **XLSXFormatter**\ *(sheet_page: str)*

    The implementation for saving data as *XLSX* format.
    It receive an option *sheet_page* which would be set as the name of first one sheet page.


JSONFormatter
---------------

*class* multirunnable.persistence.file.files.\ **JSONFormatter**\ *()*

    The implementation for saving data as *JSON* format.


Archivers Objects
==================

*module* multirunnable.persistence.file.archivers

This module responses of annotating all attributes and methods for different archiver format it should have.
Same as module *File*, it ONLY annotates behaviors but it won't tell you how to do something with them.
Currently, *MultiRunnable* provides 1 formats: *ZIP*.
They all extends from class *Archiver* to implement their details.

Archiver
--------------

*class* multirunnable.persistence.file.archivers.\ **ZIPArchiver**\ *()*

    This is the basically class to let every subclass which for different archiver format to implement details and extend features.
    It already has 2 properties for subclass: *file_path* and *mode*.


*property* **file_path**\ *()*

    The target archiver path. It could use *getting* and *setting* of this property.


*property* **mode**\ *()*

    The mode how to operate with archiver. It could use *getting* and *setting* of this property.


*abstract* **init**\ *()*

    Initial processing before compress. In generally, it would instantiate needed object like *zipfile.ZipFile*.


*abstract* **compress**\ *(data_map_list: List[namedtuple])*

    Compress the data into target archiver. The argument *data_map_list*
    receives a list of NamedTuple object which has 2 attributes *file_path* and *data*.


*abstract* **close**\ *()*

    Close the archiver IO object. Same as *File* object, it MUST to do this.


ZIPArchiver
--------------

*class* multirunnable.persistence.file.archivers.\ **ZIPArchiver**\ *()*

    The implementation for compressing data as *ZIP* format.


**init**\ *()*

    Instantiate *zipfile.ZipFile*.


Savers Objects
================

*module* multirunnable.persistence.file.saver

It's the really object which responses of how to use of saving data with different file formats (*File*) or archivers (*Archiver*).
*File* and *Archiver* annotate attributes and methods, *BaseSaver* annotates how it work finely with them.


BaseSaver
----------

*class* multirunnable.persistence.file.saver.\ **BaseSaver**\ *()*

    This is the basically class to let every subclass which for different saver to implement
    details and extend features with different file format, archiver or mediator.


*abstract* **register**\ *(mediator: BaseMediator, strategy: SavingStrategy)*

    Register saving strategy which you want to use. It would register strategy object


FileSaver
------------

*class* multirunnable.persistence.file.saver.\ **FileSaver**\ *()*

    The implementation for saving data as target format.


**register**\ *(mediator: BaseMediator, strategy: SavingStrategy)*

    Register a *Mediator* type object to let it know how could it to do (save data).


**save**\ *(file: str, mode: str, data: List[list], encoding: str = "UTF-8")*

    The truly API for client site to use to save data. This methods would return different value with different **SavingStrategy**.

    SavingStrategy:

    * ONE_THREAD_ONE_FILE
        * Main Runnable Object:
            It shouldn't do anything with this strategy.
            Hence it returns a *Do_Nothing_Flag* flag.

        * Child Runnable Object:
            It needs to save data as target format of file.
            It returns a *Done_Flag* flag after saving data.

    * ALL_THREADS_ONE_FILE
        * Main Runnable Object:
            It should wait for every runnable objects done and get the result data from them to save it as target file format.
            It returns a *Done_Flag* flag.

        * Child Runnable Object:
            It won't save data but it would return it back to main runnable object.
            It returns result data and method *has_data* would be *True*.

    * ONE_THREAD_ONE_FILE_AND_COMPRESS_ALL
        * Main Runnable Object:
            It waits for every runnable objects done and get the result data from
            It returns a *Do_Nothing_Flag* flag.

        * Child Runnable Object:
            It won't save data but it would return it back to main runnable object.
            It returns a streaming object which saving result data and method *has_data* would be *True*.


**has_data**\ *()*

    Return bool value. It's *True* if it returns data or streaming data of method *save*. Otherwise, it would be *False*.


ArchiverSaver
---------------

*class* multirunnable.persistence.file.saver.\ **ArchiverSaver**\ *()*

    The implementation for saving data and compressing data as *ZIP* format.


**register**\ *(mediator: BaseMediator, strategy: SavingStrategy)*

    Register a *Mediator* type object to let it know how could it to do (compress data).


**compress**\ *(file: str, mode: str, data: List[namedtuple])*

    The truly API for client site to use to save and compress data.


Mediators Objects
==================

*module* multirunnable.persistence.file.mediator

Literally, it's the mediator who responses of telling what things saver needs to do and what things it doesn't.
It only save simple values but it's a core references about controlling runnable objects how could they to do (save data).

SavingMediator
----------------

*class* multirunnable.persistence.file.mediator.\ **SavingMediator**\ *()*

    A basically class about saving some references to let *BasicSaver* type object to refer.


*property* **worker_id**\ *()*

    ID of runnable object(s), it maybe a thread ID, Process ID, etc. It could use *getting*, *setting* and *delete* of this property.


**is_super_worker**\ *()*

    Return a bool value. It's *True* if current runnable object is main runnable object (like main-thread or main-process) or it's *False*.


*property* **super_worker_running**\ *()*

    It's a bool value. It's *True* if it's running as main runnable object or it's *False*.


*property* **child_worker_running**\ *()*

    It's a bool value. It's *True* if it's running as children runnable object or it's *False*.


*property* **enable_compress**\ *()*

    It's a bool value. It's *True* if it needs to run compressing process or it's *False*.


Persistence Layer Objects
==========================

*module* multirunnable.persistence.file.layer

It's a FAO (File Access Object) role to let client site operate with file IO object.
It annotates some templated methods which could be used directly by subclass.
So the business logic should be here if it needs but never implement anything like
how to save data as *CSV* format file or compress to a *ZIP* file.

BaseFao
---------

*class* multirunnable.persistence.file.layer.\ **BaseFao**\ *()*

    This is the basically class to let every subclass to use it directly or extend features.
    It already has 4 methods for subclass: *save_as_json*, *save_as_csv*, *save_as_excel* and *compress_as_zip*.


**save_as_json**\ *(file: str, mode: str, data: List[list])*

    Save data as *JSON* format file.


**save_as_csv**\ *(file: str, mode: str, data: List[list])*

    Save data as *CSV* format file.


**save_as_excel**\ *(file: str, mode: str, data: List[list])*

    Save data as *XLSX* format file.


**compress_as_zip**\ *(file: str, mode: str, data: List)*

    Save and compress data which is a list of NamedTuple object has *file_path* and *data* values as *ZIP* format file.

