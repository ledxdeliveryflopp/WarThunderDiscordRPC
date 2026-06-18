from typing import Any

import gevent
from gevent import Greenlet
from loguru import logger


class GeventService:

    def __init__(self):
        self.gevent_logger = logger.bind(source='gevent')

    def spawn_task(
            self, target: callable, target_args: Any | None = None,
    ) -> Greenlet:
        self.gevent_logger.info(f'Spawn task for -> {target.__name__}')
        self.gevent_logger.info(f'Target args -> {target_args}')
        if target_args is None:
            return gevent.spawn(target)
        elif type(target_args) is list:
            return gevent.spawn(target, *target_args)
        return gevent.spawn(target, target_args)

    def run_tasks(self, tasks: list[Greenlet]) -> None:
        self.gevent_logger.info(f'Run gevent tasks -> {tasks}')
        gevent.joinall(tasks, raise_error=True)


gv_service = GeventService()
