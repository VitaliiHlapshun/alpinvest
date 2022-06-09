from backend.wsgi import remote
from backend.api.utils import CreateMovieRequest, CreateMovieResponse, \
    GetMovieRequest
from backend import api, movie
from backend.swagger import swagger


@api.endpoint(path="movie", title="Movie API")
class Movie(remote.Service):
    @swagger("Create a movie")
    @remote.method(CreateMovieRequest)
    def post(self, request):
        entity = movie.Movie.create(
            title=request.title,
            genre=request.genre,
            year=request.year,
            imdb_id=request.imdb_id)
        return CreateMovieResponse(status_code=200, message='Ok')

    @swagger("Get a movie")
    @remote.method(GetMovieRequest, CreateMovieResponse)
    def get(self, request):
        u = movie.Movie.get_single_movie(request.title)
        return CreateMovieResponse(
            status_code=200, message='Ok')
