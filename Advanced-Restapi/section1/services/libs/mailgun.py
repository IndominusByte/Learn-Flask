import os
from typing import List
from flask import render_template
from requests import Response, post

class MailGunException(Exception):
    def __init__(self,message: str):
        super().__init__(message)

class Mailgun:
    _DOMAIN_NAME = os.getenv('MAILGUN_DOMAIN_NAME')
    _API_KEY = os.getenv('MAILGUN_API_KEY')

    @classmethod
    def send_email(cls,email: List[str],subject: str, html: str, **param) -> Response:
        res = post(f"https://api.mailgun.net/v3/{cls._DOMAIN_NAME}/messages",
                auth=("api", f"{cls._API_KEY}"),
                data={"from": "dont-reply@zooka.com",
                "to": email,
                "subject": subject,
                "html": render_template(html,**param)}
        )
        if res.status_code != 200: raise MailGunException('Failed to send email')
        return res
