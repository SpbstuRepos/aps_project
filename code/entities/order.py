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

    def __init__(self, id: int, priority: int, issuer):
        self._id = id
        self._priority = priority
        self.status = Status.CREATED
        self._issuer = issuer

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def id(self):
        return self._id

    @property
    def priority(self):
        return self._priority

    @property
    def issuer(self):
        return self._issuer
