from pathlib import Path

EXTENSIONS = ("jpg", "jpeg", "png", "webp")


class AttachmentService:
    def __init__(self, folder):
        self.folder = Path(folder)

    def find(self, ticket_id):
        name = int(ticket_id)
        for path in sorted(self.folder.glob(f"{name}.*")):
            if path.suffix.lower().lstrip(".") in EXTENSIONS and path.is_file():
                return path
        return None

    def url(self, ticket_id):
        return f"/api/tickets/{int(ticket_id)}/image" if self.find(ticket_id) else None
