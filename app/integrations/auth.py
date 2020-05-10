from requests_oauthlib import OAuth2Session
import os
import logging


class Auth:
    def __init__(self):
        self.github_client = OAuth2Session(os.getenv("CLIENT_ID"))
        self.is_authenticated = False

    def get_user_info(self):
        """Obtains authenticated basic user info"""
        user_data = self.github_client.get(os.getenv("GITHUB_USER_URL"))
        user = user_data.json()
        logging.info("")
        logging.info(" ----------------------------------------------- ")
        logging.info(f"    Welcome {user['name']} - {user['login']}")
        logging.info(" ----------------------------------------------- ")

    def get_token(self, redirect_response: str):
        """Obtains a token from the redirect_response code"""
        try:
            self.github_client.fetch_token(
                os.getenv("TOKEN_URL"),
                client_secret=os.getenv("CLIENT_SECRET"),
                authorization_response=redirect_response,
            )
            self.is_authenticated = True
            self.get_user_info()
        except Exception as e:
            self.is_authenticated = False
            logging.error(f"Fetch token failed {e}")

    def get_authorization(self):
        """Redirects an user to GitHub for authorization"""
        authorization_url, state = self.github_client.authorization_url(
            os.getenv("AUTHORIZATION_BASE_URL")
        )
        logging.info("")
        logging.info(" ---------- 2 Steps Authentication Process ---------- ")
        logging.info(
            " 1. Please go to the following url and"
            f"login with your Github account: {authorization_url}"
        )
        logging.info(f" 2. Copy the complete redirected url below ")
        redirect_response = input()

        if not redirect_response:
            self.is_authenticated = False
            logging.info(f"It is necessary to insert the redirected url ")
            return

        self.get_token(redirect_response.strip())
