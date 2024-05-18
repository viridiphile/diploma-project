import logging
import logging.handlers
import queue
import threading

def setup_async_logging(level=logging.INFO):
    log_queue = queue.Queue(-1)  # No limit on size
    queue_handler = logging.handlers.QueueHandler(log_queue)
    handler = logging.StreamHandler()
    listener = logging.handlers.QueueListener(log_queue, handler)
    
    root = logging.getLogger()
    root.setLevel(level)
    root.addHandler(queue_handler)
    listener.start()
    
    return listener
