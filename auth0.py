#!/usr/bin/env python

import json
import os
import requests
import logging

class Auth0Client(object):

    def __init__(self,**kwargs):

        self.classname = "Auth0Client"
        self.logger.logging.basicConfig(level=logging.INFO)

        # (1) set AUTH0 client info

        self.auth0_client_id = os.environ["AUTH0_CLIENT_ID"]
        self.auth0_client_secret = os.environ["AUTH0_CLIENT_SECRET"]
        self.auth0_domain = os.environ["AUTH0_DOMAIN"]
        self._set_auth0_client_token()

    def _set_auth0_client_token(self):

        payload = { "client_id": self.auth0_client_id,
                    "client_secret": self.auth0_client_secret,
                    "audience": "https://{}.auth0.com/api/v2/".format(self.auth0_domain),
                    "grant_type": "client_credentials" }

        api_endpoint = 'https://{}.auth0.com/oauth/token'.format(self.auth0_domain)

        req = requests.post(api_endpoint,
                            data=json.dumps(payload),
                            headers={'content-type': 'application/json'})

        self.auth0_client_token = req.json()["access_token"].decode("utf-8")

    def _get_userinfo_frm_auth0(self,user):

        endpoint = "https://{}.auth0.com/api/v2/users/{}".format(self.auth0_domain,user)
        headers = {'Authorization': 'Bearer %s' % self.auth0_client_token}
        req = requests.get(endpoint,headers=headers)

        return req.json()

    def _get_user_access_token_with_refresh(self,**kwargs):

        payload = { "client_id": self.auth0_client_id,
                    "client_secret": self.auth0_client_secret,
                    "refresh_token": kwargs["refresh_token"].decode("utf-8"),
                    "grant_type": "refresh_token" }

        _endpt = 'https://{}.auth0.com/oauth/token'.format(self.auth0_domain)
        headers = {'content-type': 'application/json'}

        req = requests.post(_endpt,
                            data=json.dumps(payload),
                            headers=headers)
 
        return req.json()["access_token"].decode("utf-8")

    def get_user_access_token(self,user):

        # (2) get initial user info
        user_info = self._get_userinfo_frm_auth0(user)

        if str(user_info["identities"][0]["provider"]) == "bitbucket":
            # (3) try to get access token from refresh token
            user_token = self._get_user_access_token_with_refresh(user=user,**user_info["identities"][0])
        else:
            user_token = user_info["identities"][0]["access_token"].decode("utf-8")

        return user_token
