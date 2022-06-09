import os
from backend import error, user
from backend.omdb_api import Omdb
from operator import itemgetter
from google.cloud import ndb

client = ndb.Client()


class NotFound(error.Error):
    pass


class Denied(error.Error):
    pass


class OutOfRange(error.Error):
    pass


class CredentialsInvalid(error.Error):
    pass


class Movie(ndb.Model):
    """Defines movie entity"""

    title = ndb.StringProperty(required=True)
    genre = ndb.StringProperty(required=True)
    year = ndb.IntegerProperty(required=True)
    imdb_id = ndb.StringProperty(required=True)

    @classmethod
    def create(cls, title, genre, year, imdb_id):
        """Creates movie record"""
        entity = cls(
            title=title,
            genre=genre,
            year=year,
            imdb_id=imdb_id
        )
        entity.put()
        return entity

    @classmethod
    def create_test_100(cls):
        """Creates 100 test movie records based on Omdb list in case the
        model is empty"""
        if cls.check_if_empty():
            movies = Omdb.get_movies_from_omdb()
            for movie in movies:
                movie_title = movie.get('Title')
                movie_genre = movie.get('Genre')
                try:
                    movie_year = int(movie.get('Year'))
                except TypeError:
                    continue
                imdb_id = movie.get('imdbID')
                cls.create(movie_title, movie_genre, movie_year, imdb_id)
            return True
        return Denied('The database is not empty')

    @classmethod
    def check_if_empty(cls):
        """Checks if the model has no records"""
        if len(list(cls.query())) == 0:
            return True
        return False

    def __repr__(self):
        return f'"{self.title}"({self.year})'

    @classmethod
    def get_single_movie(cls, title):
        """Returns single movies by title
        Alternative:
        def get_single_movie(cls, title):
            with client.context():
                entities = cls.query(cls.title == title).fetch(1)
                return entities[0] if entities else None"""
        if cls.check_if_empty():
            entities = cls.query()
            for movie in entities:
                if movie.title != title:
                    raise NotFound(f'The movie with the title "{title}" has '
                                   f'not been found')
                return movie

    @classmethod
    def get_movies_ordered(cls, order_key, limit=10):
        """Returns index number of movies ordered by key
        Alternative:
        def get_movies_ordered(cls, order_key, index=10):
            with client.context():
            query = cls.query()
            return query.order(order_key).fetch(index)"""
        all_movies = [movie.to_dict() for movie in list(cls.query())]
        if order_key not in dir(list(cls.query())[0]):
            raise NotFound('Please, choose criteria from: "title", '
                           '"genre", "year" or "imdb_id"')
        elif limit > len(list(cls.query())):
            raise OutOfRange("Limit is out of records range")
        ordered = sorted(all_movies, key=itemgetter(order_key))
        return ordered[:limit]

    @classmethod
    def delete(cls, title, _user):
        """Deletes the movie by title if user is logged in"""
        if user.User.login(_user.credentials.email, _user.credentials.password
                           ) == _user:
            entity = Movie.query()
            for movie in entity:
                if movie.title != title:
                    raise NotFound(f'The movie with the title "{title}" '
                                   f'has not been found')
                movie.key.delete()
        raise CredentialsInvalid(
            'No user found with given email and password')


class Pagination:
    """Manages pagination of returned ordered recordset"""

    def __init__(self, movies, records_per_page):
        self.movies = movies
        self.records_per_page = records_per_page

    def movie_count(self):
        """Returned the quantity of ordered movies in collection"""
        return len(self.movies)

    def page_count(self):
        """Returns the quantity of pages"""
        if self.movie_count() % self.records_per_page == 0:
            return self.movie_count() / self.records_per_page
        return self.movie_count() // self.records_per_page + 1

    def movies_per_page(self, movies, page_number):
        """Returns the ordered movie lines per page"""
        if page_number > self.page_count():
            raise OutOfRange('Index is out of page range')
        chunked_list = list()
        for i in range(0, len(movies), self.records_per_page):
            chunked_list.append(movies[i:i + self.records_per_page])
        return f'Page {page_number}: {chunked_list[page_number - 1]}'


# if __name__ == "__main__":
    # print(Movie.create_test_100())
    # print(Movie.create(title='Gold', genre='documentary', year=2016,
    #                              imdb_id='tt191919'))
    # print(Movie.get_single_movie("Toscana"))
    # Movie.check_if_empty())
    # _ordered = Movie.get_movies_ordered('title', 2)
    # print(Movie.get_movies_ordered('title', 2))
    # paginator = Pagination(_ordered, 4)
    # print(paginator.movie_count())
    # print(paginator.page_count())
    # print(paginator.movies_per_page(_ordered, 3))
