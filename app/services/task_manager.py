from concurrent.futures import ThreadPoolExecutor

from app.services.task_interface import ITask


class TaskManager:
    def __init__(self):
        self.executor = ThreadPoolExecutor()

    def run_task(self, task: ITask):
        return self.executor.submit(task.execute)
