import os
from social.backends.oauth import BaseOAuth2

from drchrono import settings

class drchronoOAuth2(BaseOAuth2):
    """
    drchrono OAuth authentication backend
    https://drchrono.com/o/authorize/?redirect_uri=REDIRECT_URI_ENCODED&response_type=code&client_id=CLIENT_ID_ENCODED&scope=SCOPES_ENCODED
    """

    name = 'drchrono'
    AUTHORIZATION_URL = 'https://drchrono.com/o/authorize/'
    ACCESS_TOKEN_URL = 'https://drchrono.com/o/token/'
    ACCESS_TOKEN_METHOD = 'POST'
    REDIRECT_STATE = False
    KEY = settings.CLIENT_ID
    SECRET = settings.CLIENT_SECRET
    USER_DATA_URL = 'https://drchrono.com/api/users/current'
    EXTRA_DATA = [
        ('refresh_token', 'refresh_token'),
        ('expires_in', 'expires_in')
    ]
    # TODO: setup proper token refreshing
    def __init__(self, *args, **kwargs):
        # import pdb;pdb.set_trace();
        super(drchronoOAuth2, self).__init__(*args, **kwargs)

    def get_user_details(self, response):
        """
        Return user details from drchrono account
        """
        return {'username': response.get('username'),}

    def user_data(self, access_token, *args, **kwargs):
        """
        Load user data from the service
        """
        return self.get_json(
            self.USER_DATA_URL,
            headers=self.get_auth_header(access_token)
        )

    def get_auth_header(self, access_token):
        return {'Authorization': 'Bearer {0}'.format(access_token)}
