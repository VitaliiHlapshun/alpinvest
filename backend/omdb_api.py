import omdb
import requests
from imdb import Cinemagoer

API_KEY = 'fa210c68'
DATA_URL = 'http://www.omdbapi.com/?apikey=' + API_KEY


class Imdb:
    """Defines entity of data retrieved from Imdb source"""

    @staticmethod
    def get_id_list():
        """Method returns ids-list of 100 most popular movies rated by Imdb"""
        entity = Cinemagoer()
        list_100_popular = entity.get_popular100_movies()
        res = [f'tt{movie.movieID}' for movie in list_100_popular]
        return res


class Omdb:
    """Defines entity of data retrieved from  Omdb source based on Imdb
    class"""

    @staticmethod
    def get_movies_from_omdb():
        """Method gets movie details fetched by ids retrieved from Imdb"""
        omdb.set_default('apikey', API_KEY)
        movies = []
        for imdb_id in Imdb.get_id_list():
            year = ''
            params = {
                'i': imdb_id,
                'type': 'movie',
                'y': year,
                'plot': 'full'
            }
            response = requests.get(DATA_URL, params=params).json()
            if response.get('Title') == None:
                print(f'Id {imdb_id} does not exist')
                continue
            movies.append(response)
        return movies


# if __name__ == "__main__":
#     print(Omdb.get_movies_from_omdb())
