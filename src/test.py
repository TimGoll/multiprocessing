from time import sleep

import QueueHandler, MultiprocessingBase

################ USER CLASSES ################

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



		
def main():
	try:
		queueHandler = QueueHandler.QueueHandler()
		queueHandler.initQueue('main_queue')

		classReader   = ClassReader(queue_handler = queueHandler, main_queue_name = 'main_queue')
		#create another instance to demonstrate the uniqueness of the internal queue name (address)
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

if __name__ == "__main__":
	main()