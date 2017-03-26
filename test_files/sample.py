import threading
import Queue
import time

myQueue = Queue.PriorityQueue()
yourQueue = Queue.PriorityQueue()

# for x in range(10):
#     myQueue.put(x)

# while not myQueue.empty():
#     val = myQueue.get()
#     print "Outputting: ", val

# for x in range(10):
#     yourQueue.put(x)

# while not yourQueue.empty():
#     val = yourQueue.get()
#     print "Outputting: ", val