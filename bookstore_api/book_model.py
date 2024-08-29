class Book:
    def __init__(self, title, author, year, id=None) -> None:
        self.id = id
        self.title = title
        self.author = author
        self.year = year

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year
        }
