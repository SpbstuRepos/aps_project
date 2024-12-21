class Status:
    CREATED = 'created'
    QUEUED = 'queued'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    DROPPED = 'dropped'


class Order:
    # id: int
    # priority: int
    # status: str

    def __init__(self, id: int, priority: int, issuer, status_update_handler=None):
        self._id = id
        self._priority = priority
        self._issuer = issuer
        self._status_update_handler = status_update_handler
        self.status = Status.CREATED

    @property
    def status_update_handler(self):
        return self._status_update_handler

    @status_update_handler.setter
    def status_update_handler(self, value):
        self._status_update_handler = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

        if self.status_update_handler != None:
            self.status_update_handler(self)

    @property
    def id(self):
        return self._id

    @property
    def priority(self):
        return self._priority

    @property
    def issuer(self):
        return self._issuer
