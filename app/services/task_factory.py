from app.services.tasks import DNSQueryTask, HTTPGetTask, StopHTTPServerTask, StartHTTPServerTask


class TaskFactory:
    _tasks = {}

    @classmethod
    def register_task(cls, task_name, task_cls):
        cls._tasks[task_name] = task_cls

    @classmethod
    def create_task(cls, task_name, **kwargs):
        if task_name not in cls._tasks:
            raise ValueError(f"Task {task_name} not supported.")
        return cls._tasks[task_name](**kwargs)


# Register tasks
TaskFactory.register_task('dns_query', DNSQueryTask)
TaskFactory.register_task('http_get', HTTPGetTask)
TaskFactory.register_task('stop_http_server', StopHTTPServerTask)
TaskFactory.register_task('start_http_server', StartHTTPServerTask)