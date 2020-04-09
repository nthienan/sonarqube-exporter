import logging
import time

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger


class Scheduler:
    def __init__(self):
        logging.info("Initialize scheduler")
        self._scheduler = BackgroundScheduler()
        self._is_running = False

    def schedule(self, executor, interval):
        trigger = IntervalTrigger(seconds=interval)
        if trigger:
            logging.info("Scheduling sqe-executor...")
            self._scheduler.add_job(func=executor.run, trigger=trigger, name="sqe-collector")

    def start(self):
        logging.info("Scheduler is starting...")
        self._is_running = True
        self._scheduler.start()

    def is_running(self):
        return self._is_running

    def wait(self):
        while self._is_running:
            time.sleep(5)

    def shutdown(self):
        logging.info("Scheduler is shutting down...")
        self._scheduler.shutdown()
        self._is_running = False
        logging.info("Scheduler has been shutdown")
