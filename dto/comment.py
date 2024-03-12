class CommentDTO:
    def __init__(self, _id, article, body, author, created_at, updated_at, deleted_at, is_blind):
        self._id = _id
        self.article = article
        self.author = author
        self.body = body
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at
        self.is_blind = is_blind

    def to_dict(self):
        return {
            "_id": self._id,
            "article": self.article,
            "author": self.author,
            "body": self.body,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
            "is_blind": self.is_blind,
        }

    @staticmethod
    def from_dict(data):
        return CommentDTO(
            _id=data.get("_id"),
            article=data.get("article"),
            author=data.get("author"),
            body=data.get("body"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            deleted_at=data.get("deleted_at"),
            is_blind=data.get("is_blind"),
        )
