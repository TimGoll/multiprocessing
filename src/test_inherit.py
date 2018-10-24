from multiprocessing import Process, Queue, queues
from time import sleep
import os

################ LIBRARY CLASSES ################

class QueueHandler():
    def __init__(self):
        self.queues = {}
        self.flag   = 'QHDL'

    def initQueue(self, name):
        try: # check if queue already exists
            value = self.queues[name] #dummy
            print('[' + self.flag + '] [ERROR] queue with the name ' + str(name) + ' is already initialised!')
        except KeyError:
            # Key is not present; create new queue
            print('[' + self.flag + '] queue with the name ' + str(name) + ' initialised!')
            self.queues[name] = Queue()

    # PUT ELEMENT IN QUEUE
    def put(self, name, data):
        try: # check if queue exists
            self.queues[name].put(data)
        except KeyError:
            # Key is not present; create new queue
            print('[' + self.flag + '] [ERROR] queue with the name ' + str(name) + ' does not exist!')

    # GET DATA FROM QUEUE AND REMOVE ELEMENT
    def get(self, name):
        try: # check if queue exists
            try:
                return self.queues[name].get(False)
            except queues.Empty: #queue is empty
                pass
        except KeyError:
            # Key is not present; create new queue
            print('[' + self.flag + '] [ERROR] queue with the name ' + str(name) + ' does not exist!')

        return None

    # REMOVE ALL ELEMENTS AND ONLY RETURN NEWEST ELEMENT
    def get_newest(self, name):
        try: # check if queue exists
            return_data = None
            while (True):
                try:
                    return_data = self.queues[name].get(False)
                except queues.Empty: #queue is empty
                    return return_data
        except KeyError:
            # Key is not present; create new queue
            print('[' + self.flag + '] [ERROR] queue with the name ' + str(name) + ' does not exist!')

        return None


# BASE OF THE MULTIPROCESSING, HANDLES ALL DEFAULT FUNCTIONS
class MultiprocessingBase(object):
    def __init__(self, queue_handler):
        self.isRunning           = False
        self.process             = None

        self.queue_handler       = queue_handler

        self.flag                = ''

    # FROM THE OUTSIDE CALLED START FUNCTION
    def start_process(self):
        #init internal queue
        self.internal_queue_name = str(hex(id(self))) + '_' + '_internal_queue' #genrate unique name based on memory id
        self.queue_handler.initQueue(self.internal_queue_name)

        self.isRunning           = True
        self.process             = Process(target=self.internal_run_process)
        self.process.start()

    # PROCESS SPECIFIC DATA TO BE SET UP
    def init_process(self):
        pass

    def deinit_process(self):
        print ('[' + self.flag + '] process successfully stopped!')

    def stop_process(self):
        self.queue_handler.put(self.internal_queue_name, '__STOP_FLAG__')
        self.process.join() #isn't needed, processes handle joining by themself

    def internal_run_process(self):
        self.init_process()
        while (self.isRunning):
            try:
                # check if there is a stop flag
                if (self.queue_handler.get(self.internal_queue_name) == '__STOP_FLAG__'):
                    print ('[' + self.flag + '] stop flag received')
                    self.isRunning = False
                self.run_process()
            except KeyboardInterrupt:
                pass
        self.deinit_process()

    def run_process(self):
        pass




################ USER CLASSES ################

class ClassReader(MultiprocessingBase):
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

class ClassInserter(MultiprocessingBase):
    def __init__(self, queue_handler, main_queue_name):
        super(ClassInserter, self).__init__(queue_handler)
        self.main_queue_name = main_queue_name
        self.flag = 'INST'

        self.counter = 0

    def run_process(self):
        self.queue_handler.put(self.main_queue_name, self.counter)
        self.counter += 1
        sleep(0.251)


try:
    queueHandler = QueueHandler()
    queueHandler.initQueue('main_queue')

    classReader   = ClassReader(queue_handler = queueHandler, main_queue_name = 'main_queue')
    #create another instance to check the uniqueness of the queue name (address)
    classReader2  = ClassReader(queue_handler = queueHandler, main_queue_name = 'main_queue')
    classInserter = ClassInserter(queue_handler = queueHandler, main_queue_name = 'main_queue')

    classReader.start_process()
    classReader2.start_process()
    classInserter.start_process()

    while (True): #keep main process alive
        sleep(1)
except KeyboardInterrupt:
    classReader.stop_process()
    classReader2.stop_process()
    classInserter.stop_process()
    pass
