from typing import List
import os
from flask import request, url_for
from requests import Response, post

from claims_solutions_api.errors import InternalServerError

class Mailgun:
    @classmethod
    def send_email(cls, email: List[str], subject, text, html) -> Response:
        
        try:
            title = f"{os.environ['EMAIL_TITLE']} <{os.environ['MAILGUN_EMAIL']}>"
            response = post(
                os.environ['MAILGUN_API_URL'],
                auth=("api", os.environ['MAILGUN_API_KEY']),
                data={
                    "from": title,
                    "to": email,
                    "subject": subject,
                    "text": text,
                    "html": html
                }
            )
        except KeyError:
            #
            # Throwing the "InternalServerError" exception here because catching
            # the "KeyError" means we didn't have the enviroment variables set
            # up correctly.
            #
            raise InternalServerError
        
        if response.status_code != 200:
            raise InternalServerError

        return response