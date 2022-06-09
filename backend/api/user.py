import time
from backend.api.utils import *

from backend.wsgi import remote, message_types

from backend import api, user
from backend.oauth2 import oauth2, Oauth2
from backend.swagger import swagger


@api.endpoint(path="user", title="User API")
class User(remote.Service):
    @swagger("Create a user")
    @remote.method(CreateRequest, TokenResponse)
    def create(self, request):
        u = user.User.create(email=request.email, password=request.password, name=request.name)
        session = Oauth2.create(u.key)

        return TokenResponse(
            access_token=session.access_token.token,
            expires=time.mktime(session.access_token.expires.timetuple()),
            refresh_token=session.refresh_token.token
        )

    @swagger("Renew user token")
    @remote.method(TokenRequest, TokenResponse)
    def token(self, request):
        session = Oauth2.renew(request.access_token, request.refresh_token)

        return TokenResponse(
            access_token=session.access_token.token,
            expires=time.mktime(session.access_token.expires.timetuple()),
            refresh_token=session.refresh_token.token
        )

    @swagger("User login")
    @remote.method(LoginRequest, TokenResponse)
    def login(self, request):
        user_key = user.User.login(request.email, request.password).key
        session = Oauth2.create(user_key)

        return TokenResponse(
            access_token=session.access_token.token,
            expires=time.mktime(session.access_token.expires.timetuple()),
            refresh_token=session.refresh_token.token
        )

    @swagger("User logout")
    @oauth2.required()
    @remote.method(message_types.VoidMessage, message_types.VoidMessage)
    def logout(self, request):
        self.session.revoke()
        return message_types.VoidMessage()

    @swagger("Get a user")
    @oauth2.required()
    @remote.method(GetRequest, GetResponse)
    def get(self, request):
        u = user.User.get(request.id)
        return GetResponse(
            id=u.id,
            name=u.name
        )

    @oauth2.required()
    @remote.method(message_types.VoidMessage, EmailVerifiedResponse)
    def email_verified(self, request):
        return EmailVerifiedResponse(
            email_verified=self.session.user.email_verified
        )

    @oauth2.required()
    @remote.method(message_types.VoidMessage, MeResponse)
    def me(self, request):
        u = self.session.user
        return MeResponse(
            id=u.id,
            email=u.email,
            email_verified=u.email_verified,
            name=u.name,
            phone=u.phone
        )

    @swagger("Search users")
    @oauth2.required()
    @remote.method(SearchRequest, SearchResponse)
    def search(self, request):
        users = []
        if "@" in request.search:
            users = [user.User.get_by_email(request.search)]
        else:
            users = user.User.search(request.search, offset=request.offset)

        return SearchResponse(users=[SearchResult(
            id=u.id,
            name=u.name
        ) for u in users if u is not None])

    @swagger("Update password")
    @oauth2.required()
    @remote.method(UpdatePasswordRequest, message_types.VoidMessage)
    def update_password(self, request):
        self.session.user.update_password(current_password=request.current_password, password=request.password)
        return message_types.VoidMessage()

    @swagger("Update email")
    @oauth2.required()
    @remote.method(UpdateEmailRequest, message_types.VoidMessage)
    def update_email(self, request):
        self.session.user.update_email(current_password=request.current_password, email=request.email)
        return message_types.VoidMessage()

    @swagger("Update a user")
    @oauth2.required()
    @remote.method(UpdateRequest, message_types.VoidMessage)
    def update(self, request):
        self.session.user.update(**api.message_to_dict(request))
        return message_types.VoidMessage()
