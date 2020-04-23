import os
from typing import List
from requests import post
from flask import render_template

class MailGunException(Exception):
    def __init__(self,message: str):
        super().__init__(message)

class MailGun:
    DOMAIN_NAME = os.getenv("MAILGUN_DOMAIN_NAME")
    API_KEY = os.getenv("MAILGUN_API_KEY")

    @classmethod
    def send_email(self,email: List,subject: str, html: str, **param):
        if not self.DOMAIN_NAME: raise MailGunException('Domain name failed to load')
        if not self.API_KEY: raise MailGunException('Api key failed to load')

        res = post("https://api.mailgun.net/v3/{}/messages".format(self.DOMAIN_NAME),
                auth=("api", self.API_KEY),
                data={"from": "Excited User <mailgun@zooka.com>",
                "to": email,
                "subject": subject,
                "html": render_template(html,**param)})

        if res.status_code != 200: raise MailGunException("Failed to send email")
