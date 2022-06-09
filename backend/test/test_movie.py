from backend import test, user, movie


class TestMovie(test.TestCase):

    def test_create_test_100(self):
        obj = movie.Movie.create_test_100()
        self.assertTrue(obj, movie.Movie.create_test_100())

    def test_create(self):
        obj = movie.Movie.create(title='Gold', genre='documentary', year=2016,
                                 imdb_id='tt191919')
        self.assertTrue(obj.year == 2016)
        self.assertTrue(obj.genre == 'documentary')
        self.assertFalse(obj.imdb_id == 'tt19191999')

    def test_check_if_empty(self):
        self.assertTrue(movie.Movie.check_if_empty())

    def test_get_single_movie(self):
        self.assertEqual(None, movie.Movie.get_single_movie('Title'))

    def test_delete(self):
        user_obj = user.User.create("test@gmail.com", "test3")
        self.assertRaises(user.CredentialsInvalid, lambda:
        movie.Movie.delete('Toscana', user_obj))


class TestPagination(test.TestCase):

    def test_movie_count(self):
        collection = [{'genre': 'documentary', 'imdb_id': 'tt191919',
                       'title': 'Movie1', 'year': 2018},
                      {'genre': 'documentary', 'imdb_id': 'tt191919',
                       'title': 'Movie2', 'year': 2017},
                      {'genre': 'documentary', 'imdb_id': 'tt191919',
                       'title': 'Movie3', 'year': 2017},
                      {'genre': 'documentary', 'imdb_id': 'tt191919',
                       'title': 'Movie4', 'year': 2017},
                      {'genre': 'documentary', 'imdb_id': 'tt191919',
                       'title': 'Movie5', 'year': 2017},
                      {'genre': 'documentary', 'imdb_id': 'tt191919',
                       'title': 'Movie6', 'year': 2017}]
        obj = movie.Pagination(collection, 2)
        self.assertEqual(6, movie.Pagination.movie_count(obj))

    def test_page_count(self):
        collection = [{'genre': 'documentary', 'imdb_id': 'tt191919',
                       'title': 'Movie1', 'year': 2018},
                      {'genre': 'documentary', 'imdb_id': 'tt191919',
                       'title': 'Movie2', 'year': 2017},
                      {'genre': 'documentary', 'imdb_id': 'tt191919',
                       'title': 'Movie3', 'year': 2017},
                      {'genre': 'documentary', 'imdb_id': 'tt191919',
                       'title': 'Movie4', 'year': 2017},
                      {'genre': 'documentary', 'imdb_id': 'tt191919',
                       'title': 'Movie5', 'year': 2017},
                      {'genre': 'documentary', 'imdb_id': 'tt191919',
                       'title': 'Movie6', 'year': 2017}]
        obj = movie.Pagination(collection, 2)
        self.assertEqual(3, movie.Pagination.page_count(obj))

    def test_movies_per_page(self):
        collection = [{'genre': 'documentary', 'imdb_id': 'tt191919',
                       'title': 'Movie1', 'year': 2018},
                      {'genre': 'documentary', 'imdb_id': 'tt191919',
                       'title': 'Movie2', 'year': 2017},
                      {'genre': 'documentary', 'imdb_id': 'tt191919',
                       'title': 'Movie3', 'year': 2017},
                      {'genre': 'documentary', 'imdb_id': 'tt191919',
                       'title': 'Movie4', 'year': 2017},
                      {'genre': 'documentary', 'imdb_id': 'tt191919',
                       'title': 'Movie5', 'year': 2017},
                      {'genre': 'documentary', 'imdb_id': 'tt191919',
                       'title': 'Movie6', 'year': 2017}]
        obj = movie.Pagination(collection, 2)
        self.assertRaises(movie.OutOfRange, lambda:
        movie.Pagination.movies_per_page(obj, collection, 4))


class TestMovieApi(test.TestCase):

    def test_post(self):
        resp = self.api_client.post("movie.create",
                                    dict(title='Gold', genre='documentary',
                                         year=2016, imdb_id='tt191919'))
        self.assertEqual(resp.get("code"), None)
        resp = self.api_client.get("movie.get", dict(title=resp.get('Gold')))
        self.assertEqual(resp.get("code"), None)
