import requests
from requests.auth import HTTPBasicAuth
import json
import Jira_get_started as jira_start
from MailFiles import send_mail

class Confluence:

    base_url = ""
    url = ""
    mail_body = {}

    def __init__(self, base_url, access_token, user_email):
        self.base_url = base_url
        self.auth = HTTPBasicAuth(user_email, access_token)

    def getAllSpaces(self, **args):
        url = "/wiki/rest/api/space"
        api = self.base_url+url
        headers = {
            "Accept": "application/json"
        }
        response = requests.request(
            'GET',
            api,
            auth=self.auth,
            headers=headers
        )
        print(response.text)

    def createSpace(self, **args):
        spacename = args["space name"]
        spacekey = spacename[:3].upper()
        url = "/wiki/rest/api/space"
        api = self.base_url+url
        headers = {
            "Accept" : "application/json",
            "Content-Type" : "application/json"
        }
        payload = json.dumps({
            "key" : spacekey,
            "name" : spacename
        })
        response = requests.request(
            'POST',
            api,
            auth=self.auth,
            data=payload,
            headers=headers
        )
        print(response.text)

    def createPrivateSpace(self, **args):
        spacename = args["space name"]
        spacekey = spacename[:3].upper()
        url = "/wiki/rest/api/space/_private"
        api = self.base_url+url
        headers = {
            "Accept" : "application/json",
            "Content-Type" : "application/json"
        }
        payload = json.dumps({
            "key" : spacekey,
            "name" : spacename
        })
        response = requests.request(
            'POST',
            api,
            auth=self.auth,
            data=payload,
            headers=headers
        )
        print(response.text)

    def getSpace(self, **args):
        spacekey = args["space key"]
        url = "/wiki/rest/api/space/"+spacekey
        api = self.base_url+url
        headers = {
            "Accept" : "application/json"
        }
        response = requests.request(
            'GET',
            api,
            auth=self.auth,
            headers=headers
        )
        print(response.text)

    def updateSpaceDescription(self, **args):
        spacekey = args["space key"]
        # spacename = all_spaces[spacekey]["name"]
        spacename = args["space name"]
        description = args["description"]
        url = "/wiki/rest/api/space/"+spacekey
        api = self.base_url+url
        headers = {
            "Accept" : "application/json",
            "Content-Type" : "application/json"
        }
        payload = json.dumps({
            "name" : spacename,
            "description" : {
                "plain" : {
                    "value" : description
                }
            }
        })
        response = requests.request(
            'PUT', 
            api,
            auth=self.auth,
            headers=headers,
            data=payload
        )
        print(response.text)

    def getSpaceContent(self, **args):
        spacekey = args["space key"]
        url = "/wiki/rest/api/content"
        api = self.base_url+url
        headers = {
            "Accpet" : "application/json"
        }
        # query = {
        #     "spaceKey" = spacekey
        # }
        response = requests.request(
            "GET",
            api,
            auth=self.auth,
            headers=headers,
            # params=query
        )
        print(response.text)

    def createContent(self, **args):
        spacekey = args["space key"]
        title = args["title"]
        description = args["description"]
        url = "/wiki/rest/api/content"
        api = self.base_url+url
        headers = {
            "Accept" : "application/json",
            "Content-Type" : "application/json"
        }
        payload = json.dumps({
            "title" : title,
            "space" : {
                "key" : spacekey
            },
            "type" : "page",
            "status" : "draft",
            "body" : {
                "export_view" : {
                    "value" : description,
                    "representation" : "view"
                }
            }
        })
        response = requests.request(
            "POST",
            api,
            headers=headers,
            data=payload,
            auth=self.auth
        )
        print(response.text)

    def search(self, **args):
        queryword = args["query"]
        cql = "text ~ '{0}'".format(queryword)
        url = "/wiki/rest/api/search"
        api = self.base_url+url
        headers = {
            "Accept" : "application/json"
        }
        query = {
            "cql" : cql
        }
        response = requests.request(
            "GET",
            api,
            headers=headers,
            params=query,
            auth=self.auth
        )
        print(response.text)