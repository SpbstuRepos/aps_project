from types import coroutine


class TaskList:
    # Items are stored as tuples (timestamp, task)

    def __init__(self):
        self._list = list()

    def empty(self):
        return len(self._list) == 0

    def pop_front(self):
        try:
            return self._list.pop(0)
        except IndexError:
            raise StopIteration()

    def yield_task(self, task, default_timestamp):
        try:
            front = self._list[0]
        except IndexError:
            front = None

        timestamp = front[0] if front != None else default_timestamp
        self.schedule_task(task, timestamp + 0.001)

    def schedule_task(self, task, timestamp):
        match_index = None

        for i in range(len(self._list)):
            time = self._list[i][0]
            if time > timestamp:
                match_index = i
                break

        if match_index != None:
            self._list.insert(match_index, (timestamp, task))
        else:
            self._list.append((timestamp, task))

    def long_wait_task(self, task, default_timestamp):
        try:
            back = self._list[-1]
        except IndexError:
            back = None

        timestamp = back[0] if back != None else default_timestamp
        self.schedule_task(task, timestamp)


class SimulationAsyncRuntime:
    def __init__(self):
        self._timestamp = 0.0
        self._tasks = TaskList()

    def create_task(self, coro):
        """Wrap a coroutine into a task and schedule it immediately."""
        self._tasks.yield_task(coro, self._timestamp)

    @property
    def timestamp(self):
        return self._timestamp

    def run(self):
        """Run tasks in the queue until all are completed."""
        while not self._tasks.empty():
            try:
                timestamp, task = self._tasks.pop_front()
                self._timestamp = timestamp
                result = task.send(None)
                if isinstance(result, Yield):
                    self._tasks.yield_task(task, self._timestamp)
                if isinstance(result, LongWait):
                    self._tasks.long_wait_task(task, self._timestamp)
                elif isinstance(result, Sleep):
                    timestamp = self._timestamp + result.dur
                    self._tasks.schedule_task(task, timestamp)
            except StopIteration:
                pass


class Yield:
    pass


class LongWait:
    pass


class Sleep:
    def __init__(self, dur: float):
        self.dur = dur


@coroutine
def yield_task():
    """Simulate a non-blocking sleep by yielding control back to the runtime."""
    yield Yield()


@coroutine
def long_wait():
    """Schedule current task to the end of execution queue."""
    yield LongWait()


@coroutine
def sleep(duration: float):
    """Simulate a non-blocking sleep by yielding control back to the runtime."""
    yield Sleep(duration)


simulated_runtime = SimulationAsyncRuntime()
