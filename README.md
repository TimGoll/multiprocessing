# Python Multiprocessing
Multiprocessing is vastly superior to threading because it creates real parallel running threads. Therefore you have to pass the data through queues. These two given classes will handle everything for you.

Tested with `Python 2.7`

## Multiprocessing Basics
Python multiprocessing works as follows: As soon as you start the process, all variables of the previously created class get copied into the new process. Therefore you can define as many vairables as you like before you start the process, but you can't change the values afterwards. This is the reason why queues are needed. They are threadsafe and allow communication between different processes.

## Example
In the following text we're discussing the topic based on a simple read/write program, where one thread sets the data and another thread reads it.

You start with inheriting the baseclass and setting up the initial data, the init function is defined as `__init__(self, obj_ptr_queue_handler, str_queue_name_1, str_queue_name_2, ... , user_args)`.

```python
import QueueHandler, MultiprocessingBase

class ClassReader(MultiprocessingBase.MultiprocessingBase):
    def __init__(self, queue_handler, main_queue_name):
        super(ClassReader, self).__init__(queue_handler)
        self.main_queue_name = main_queue_name
        self.flag = 'REDR'
        
class ClassWriter(MultiprocessingBase.MultiprocessingBase):
    def __init__(self, queue_handler, main_queue_name):
        super(ClassInserter, self).__init__(queue_handler)
        self.main_queue_name = main_queue_name
        self.flag = 'WRTR'
        
        self.counter = 0
```

In both classes the parents class `__init__` mathod has to get called first via `super`. `queue_handler` is a necessary argument, because it is the object pointer to the queue handler which is needed, even if you don't need to use queues, because the process uses an internal queue to communicate, especially to stop the process when you call the stop function. `main_queue_name` is a string and not necessary. You can pass as many queue_names and user specific arguments as you'd like to.

In the next step you have to overwrite `init_process`, `run_process` and `deinit_process`. None of them is mendatory, but at least `run_process` should be used´and is already a loop.

Therefore the finished classes look like this:
```python
class ClassReader(MultiprocessingBase.MultiprocessingBase):
    def __init__(self, queue_handler, main_queue_name):
        super(ClassReader, self).__init__(queue_handler)
        self.main_queue_name = main_queue_name
        self.flag = 'REDR'

    def run_process(self):
        #super(ClassReader, self).run_process()
        data = self.queue_handler.get(self.main_queue_name)
        if (data != None):
            print('read data: ' + str(data))
        sleep(0.1)

class ClassInserter(MultiprocessingBase.MultiprocessingBase):
    def __init__(self, queue_handler, main_queue_name):
        super(ClassInserter, self).__init__(queue_handler)
        self.main_queue_name = main_queue_name
        self.flag = 'INST'

        self.counter = 0

    def run_process(self):
        self.queue_handler.put(self.main_queue_name, self.counter)
        self.counter += 1
        sleep(0.251)
```

To run your code, you have to create instances of your classes and then start the processes. **Important note:** Always stop processes after you've started them or you get ghost processes running forever in the background.
```python
queueHandler = QueueHandler.QueueHandler()
queueHandler.initQueue('main_queue')

classReader   = ClassReader(queue_handler = queueHandler, main_queue_name = 'main_queue')
#create another instance to demonstrate the uniqueness of the internal queue name (address)
classReader2  = ClassReader(queue_handler = queueHandler, main_queue_name = 'main_queue')
classInserter = ClassInserter(queue_handler = queueHandler, main_queue_name = 'main_queue')

classReader.start_process()
classReader2.start_process()
classInserter.start_process()

#...

classReader.stop_process()
classReader2.stop_process()
classInserter.stop_process()
```

The console output of this code looks like this:
```
[QHDL] queue with the name main_queue initialised!
[QHDL] queue with the name ClassReader_0x30174d0__internal_queue initialised!
[QHDL] queue with the name ClassReader_0x3017510__internal_queue initialised!
[QHDL] queue with the name ClassInserter_0x3017530__internal_queue initialised!
[REDR] process initialized!
[REDR] process initialized!
[INST] process initialized!
read data: 0
read data: 1
read data: 2
read data: 3
read data: 4
read data: 5
read data: 6
read data: 7
read data: 8
[REDR] stop flag received
[REDR] stop flag received
[REDR] process successfully stopped!
[REDR] process successfully stopped!
[INST] stop flag received
[INST] process successfully stopped!
```

You can find this example as an executable python script in this repository.