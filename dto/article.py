class ArticleDTO:
    def __init__(self, _id, topic, author, title, date, is_blind):
        self._id = _id
        self.topic = topic
        self.author = author
        self.title = title
        self.date = date
        self.is_blind = is_blind

    def to_dict(self):
        return {
            "_id": self._id,
            "topic": self.topic,
            "author": self.author,
            "title": self.title,
            "date": self.date,
            "is_blind": self.is_blind
        }

    @staticmethod
    def from_dict(data):
        return ArticleDTO(
            _id=data.get("_id"),
            topic=data.get("topic"),
            author=data.get("author"),
            title=data.get("title"),
            date=data.get("date"),
            is_blind=data.get("is_blind")
        )
