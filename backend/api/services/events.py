class EventService:
    def __init__(self, repository):
        self.repository = repository

    def all(self):
        return self.repository.all()
