class ArticleDTO:
    def __init__(self, _id, topic, author, title, body, created_at, updated_at, deleted_at, is_blind, likes, comments):
        self._id = _id
        self.topic = topic
        self.author = author
        self.title = title
        self.body = body
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at
        self.is_blind = is_blind
        self.likes = likes
        self.comments = comments

    def to_dict(self):
        return {
            "_id": self._id,
            "topic": self.topic,
            "author": self.author,
            "title": self.title,
            "body": self.body,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
            "is_blind": self.is_blind,
            "likes": self.likes,
            "comments": self.comments
        }

    @staticmethod
    def from_dict(data):
        return ArticleDTO(
            _id=data.get("_id"),
            topic=data.get("topic"),
            author=data.get("author"),
            title=data.get("title"),
            body=data.get("body"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            deleted_at=data.get("deleted_at"),
            is_blind=data.get("is_blind"),
            likes=data.get("likes"),
            comments=data.get("comments")
        )
