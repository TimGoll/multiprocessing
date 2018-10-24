# Python Multiprocessing
Multiprocessing is vastly superior to threading because it creates real parallel running threads. Therefore you have to pass the data through queues.

Code example code of a multiprocessing project with queue handling, all user classes should inherit `MultiprocessingBase` to get all features without code duplication. Important: Always call `<instance>.stop_process()` after you started a process to prevent infinite running background tasks.

Tested with `Python 2.7`
