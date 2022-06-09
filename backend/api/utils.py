from backend.wsgi import messages


class CreateMovieRequest(messages.Message):
    title = messages.StringField(1, required=True)
    genre = messages.StringField(2, required=True)
    year = messages.IntegerField(3, required=True)
    imdb_id = messages.StringField(4, required=True)


class CreateMovieResponse(messages.Message):
    status_code = messages.IntegerField(1)
    message = messages.StringField(2)


class GetMovieRequest(messages.Message):
    title = messages.StringField(1, required=True)


class CreateRequest(messages.Message):
    email = messages.StringField(1, required=True)
    password = messages.StringField(2, required=True)
    name = messages.StringField(3)


class TokenRequest(messages.Message):
    access_token = messages.StringField(1, required=True)
    refresh_token = messages.StringField(2, required=True)


class TokenResponse(messages.Message):
    access_token = messages.StringField(1)
    expires = messages.FloatField(2)
    refresh_token = messages.StringField(3)


class LoginRequest(messages.Message):
    email = messages.StringField(1)
    password = messages.StringField(2)


class GetRequest(messages.Message):
    id = messages.StringField(1, required=True)


class GetResponse(messages.Message):
    id = messages.StringField(1)
    name = messages.StringField(2)


class EmailVerifiedResponse(messages.Message):
    email_verified = messages.BooleanField(1)


class MeResponse(messages.Message):
    id = messages.StringField(1)
    email = messages.StringField(2)
    email_verified = messages.BooleanField(3)
    name = messages.StringField(4)
    phone = messages.StringField(5)


class SearchRequest(messages.Message):
    search = messages.StringField(1, required=True)
    offset = messages.IntegerField(2, default=0)


class SearchResult(messages.Message):
    id = messages.StringField(1)
    name = messages.StringField(2)


class SearchResponse(messages.Message):
    users = messages.MessageField(SearchResult, 1, repeated=True)


class UpdatePasswordRequest(messages.Message):
    current_password = messages.StringField(1, required=True)
    password = messages.StringField(2, required=True)


class UpdateEmailRequest(messages.Message):
    current_password = messages.StringField(1, required=True)
    email = messages.StringField(2, required=True)


class UpdateRequest(messages.Message):
    name = messages.StringField(1)
    phone = messages.StringField(2)
