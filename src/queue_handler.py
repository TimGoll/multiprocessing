from multiprocessing import Queue, queues

class QueueHandler():
    def __init__(self):
        self.queues = {}
        self.flag   = 'QHDL'

    def initQueue(self, name):
        try: # check if queue already exists
            self.queues[name] # try accessing this queue
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

    # GET READER ELEMENT
    def get_reader(self, name):
        try: # check if queue exists
            return self.queues[name]._reader
        except KeyError:
            # Key is not present; create new queue
            print('[' + self.flag + '] [ERROR] queue with the name ' + str(name) + ' does not exist!')

        return None