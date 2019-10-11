import multiprocessing

class MultiprocessingBase(object):
    def __init__(self, queue_handler):
        self.isRunning     = False
        self.process       = None

        self.queue_handler = queue_handler

        self.flag          = ''

    # FROM THE OUTSIDE CALLED START/STOP METHODS
    def start_process(self):
        #init internal queue
        self.internal_queue_name = self.__class__.__name__ + '_' + str(hex(id(self))) + '_' + '_internal_queue' #genrate unique name based on memory id
        self.queue_handler.initQueue(self.internal_queue_name)

        self.isRunning     = True
        self.process       = multiprocessing.Process(target=self.__run_process__)
        self.process.start()

    def stop_process(self):
        self.queue_handler.put(self.internal_queue_name, '__STOP_FLAG__')

    # INTERNAL METHODS
    def __run_process__(self):
        self.__init_process__()
        while (self.isRunning):
            try:
                self.run_process()

                # check if there is a stop flag
                if (self.queue_handler.get(self.internal_queue_name) == '__STOP_FLAG__'):
                    print ('[' + self.flag + '] stop flag received')
                    self.isRunning = False
            except KeyboardInterrupt:
                pass
        self.__deinit_process__()

    def __init_process__(self):
        print ('[' + self.flag + '] process initialized!')
        self.init_process()

    def __deinit_process__(self):
        print ('[' + self.flag + '] process successfully stopped!')
        self.deinit_process()

    # METHODS TO BE OVERWRITTEN
    def run_process(self):
        pass

    def init_process(self):
        pass

    def deinit_process(self):
        pass

    # PASSTHROUGH FROM MULTIPROCESSING
    def wait(self, object_list, timeout = None):
        # The wait function waits for all defined objects and the internal queue to make
        # sure the internal messages are always transmitted
        multiprocessing.connection.wait(
            object_list + [self.queue_handler.get_reader(self.internal_queue_name)],
            timeout
        )
