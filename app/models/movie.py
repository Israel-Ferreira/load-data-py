class Movie:

    def __init__(self, id,  title,  year, genres) -> None:
        self.id =  id
        self.title = title
        self.year =  year
        self.genres = genres


    def __repr__(self) -> str:
        return f"Movie({self.id}, {self.title}, {self.year}, {self.genres})"
    

    def __str__(self) -> str:
        return f"Title: {self.title}, Year: {self.year}, Genres: {self.genres}"


    def to_dict(self) -> dict:
        return self.__dict__

    

    