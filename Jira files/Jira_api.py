import requests
import requests
from requests.auth import HTTPBasicAuth
import json
import Jira_get_started as jira
import sys

sys.path.append("E:\\Projects\\IPM\\Mail files")
sys.path.append("E:\\Projects\\IPM\\Input Output files")
sys.path.append("E:\\Projects\\IPM")

import config_file
import send_mail
import Text_to_Speech as speak

class Jira(object):

	base_url = config_file.JIRA_BASE_URL
	auth = HTTPBasicAuth(config_file.JIRA_USER_EMAIL, config_file.JIRA_ACCESS_TOKEN)
	all_projects = jira.getAllProjects() # get all the projects in the jira workspace
	all_users = jira.getAllUsers() # get all the users in the jira workspace
	output = ""
	mail_body = dict()

	def getSpecificProjectDetails(self, project_id):
		url = '/rest/api/2/project/'+project_id
		api = self.base_url + url
		headers = {
			"Accept": "application/json"
		}
		response = requests.request(
			"GET",
			api,
			auth=self.auth,
			headers=headers
		)
		if response.status_code != 200:
			self.output = "Project not found in the workshape or dont have required permissions"
		else:
			response = json.loads(response.text)
			self.output = "Project {name} is found. Its lead name is {lead_name}".format(name=response["name"], lead_name=response["lead"]["displayName"])
			self.mail_body = {
				"Project name":response["name"],
				"Project ID":response["id"],
				"Project key":response["key"],
				"Project lead name":response["lead"]["displayName"],
				"Project lead ID":response["lead"]["accountId"] 
			}
			speak.say(self.output)
			send_mail.sendMail(self.mail_body)

	def createNewProject(self, project_key, project_name, project_type_key, project_template_key, lead_account_id, assignee_type):
		url = '/rest/api/2/project'
		api = self.base_url + url
		headers = {
			"Accept": "application/json",
			"Content-Type": "application/json"
		}
		payload = json.dumps({
			"key"                : project_key,
			"name"               : project_name,
			"projectTypeKey"     : project_type_key,
			"projectTemplateKey" : project_template_key,
			"leadAccountId"      : lead_account_id,
			"assigneeType"       : assignee_type
		})
		response = requests.request(
			"POST",
			api,
			auth=self.auth,
			headers=headers,
			data=payload
			)
		if response.status_code != 201:
			self.output = "Request is not valid"
			speak.say(self.output)
		else:
			response = json.loads(response.text)
			self.getSpecificProjectDetails(str(response["id"]))

	def deleteProject(self, project_key):
		url = "/rest/api/2/project/"+project_key
		api = self.base_url + url
		headers = {
			"Accept": "application/json"
		}
		response = requests.request(
			"DELETE",
			api,
			auth=self.auth,
			headers=headers
		)
		if response.status_code != 204:
			self.output = "Project cant be deleted"
		else:
			self.output = "Project successfully deleted"
			self.mail_body = {
				"Status" : "Delete project success",
				"Project key" : project_key
			}
			send_mail.sendMail(self.mail_body)
		speak.say(self.output)

	def getCreateIssueMetadata(self):
		url = "/rest/api/2/issue/createmeta"
		api = self.base_url + url
		headers = {
			"Accept": "application/json"
		}
		response = requests.request(
			"GET",
			api,
			auth=self.auth,
			headers=headers
			)
		print(response)
		print(response.text)

	def createIssue(self, summary, project_id, issue_id):
		# for epic, epic name is needed
		# for subtask, there should be a parent id
		# issue types: 10000(epic), 10001(story), 10002(task), 10003(subtask), 10004(bug) 
		url = "/rest/api/2/issue"
		api = self.base_url + url
		headers = {
			"Accept": "application/json",
			"Content-Type": "application/json"
		}
		payload = json.dumps({
			"fields": {
				"summary"    : summary,
				# "parent"     : {"id" : "10017"},
				"project"    : {"id" : project_id},
				"issuetype"  : {"id": issue_id},
				# "description": description,
				# "reporter"   : {"id": reporter},
				# "assignee"   : {"name": "Tarun Agarwal"},
				# "priority"   : {"id": "2"}
			}
		})
		response = requests.request(
			"POST",
			api,
			auth=self.auth,
			headers=headers,
			data=payload
		)
		if response.status_code != 201:
			self.output = "Error in issue creation"
		else:
			response = json.loads(response.text)
			self.output = "Issue created successfully with id {id} and key {key}".format(id=response["id"], key=response["key"])
			self.mail_body = {
				"Issue id": response["id"],
				"Issue key": response["key"]
			}
			send_mail.sendMail(self.mail_body)
		speak.say(self.output)

	def getIssue(self, issue_key):
		url = "/rest/api/3/issue/"+issue_key
		api = self.base_url + url
		headers = {
			"Accept": "application/json"
		}
		response = requests.request(
			"GET",
			api,
			auth=self.auth,
			headers=headers
			)
		if response.status_code != 200:
			self.output = "Error getting issue details"
		else:
			response = json.loads(response.text)
			self.output = "Issue is created by {creator} and reported by {reporter} in project {project} and has the summary {summary}. Its priority is {priority}".format(creator=response["fields"]["creator"]["displayName"], reporter=response["fields"]["reporter"]["displayName"], project=response["fields"]["project"]["name"], summary=response["fields"]["summary"], priority=response["fields"]["priority"]["name"])
			self.mail_body = {
				"Issue key" : issue_key,
				"creator"   : response["fields"]["creator"]["displayName"],
				"reporter"  : response["fields"]["reporter"]["displayName"],
				"project"   : response["fields"]["project"]["name"],
				"summary"   : response["fields"]["summary"],
				"priority"  : response["fields"]["priority"]["name"],
			}
			send_mail.sendMail(self.mail_body)
		speak.say(self.output)

	def deleteIssue(self, issue_key):
		url = "/rest/api/2/issue/"+issue_key
		api = self.base_url + url
		headers = {
			"Accept": "application/json"
		}
		response = requests.request(
			"DELETE",
			api,
			auth=self.auth,
			headers=headers
			)
		if response.status_code != 204:
			self.output = "Error deleting the issue"
		else:
			self.output = "Issue deleted successfully"
			self.mail_body = {
				"Status" : "Issue delete success",
				"Issue key" : issue_key
			}
			send_mail.sendMail(self.mail_body)
		speak.say(self.output)

	def assignIssue(self, issue_key, accountId):
		url = "/rest/api/2/issue/"+issue_key+"/assignee"
		api = self.base_url + url
		headers = {
			"Accept": "application/json",
			"Content-Type": "application/json"
		}
		payload = json.dumps({
			"accountId" : accountId
		})
		response = requests.request(
			"PUT",
			api,
			data=payload,
			auth=self.auth,
			headers=headers
			)
		if response.status_code != 204:
			self.output = "Error assigning the issue"
		else:
			self.output = "Issue assigned successfully to {person}".format(person=self.all_users[accountId]["Name"])
			self.mail_body = {
				"Status" : "Issue assign successfully",
				"Issue key" : issue_key,
				"Assignee" : accountId
			}
			send_mail.sendMail(self.mail_body)
		speak.say(self.output)

	def getTransitions(self, issue_id):
		url = "/rest/api/2/issue/"+issue_id+"/transitions"
		api = self.base_url + url
		headers = {
			"Accept": "application/json"
		}
		response = requests.request(
			"GET",
			api,
			headers=headers,
			auth=self.auth
			)
		print(response)
		print(response.text)

	def issueTransition(self, issue_key, transition_id):
		transition = {"11":"to do", "21":"in progress", "31":"done"}
		url = "/rest/api/2/issue/"+issue_key+"/transitions"
		api = self.base_url + url
		headers = {
			"Accept": "application/json",
			"Content-Type": "application/json"
		}
		payload = json.dumps({
			"transition" : {"id":transition_id}
			# "fields"     : {"assignee": {"name" : assignee_name}}
		})
		response = requests.request(
			"POST",
			api,
			data=payload,
			headers=headers,
			auth=self.auth
			)
		if response.status_code != 204:
			self.output = "Error making issue transition"
		else:
			self.output = "Issue is transit to {type}".format(type=transition[transition_id])
			self.mail_body = {
				"Status" : "Issue transition success",
				"Issue key" : issue_key,
				"Transition level" : transition[transition_id]
			}
			send_mail.sendMail(self.mail_body)
		speak.say(self.output)

jira = Jira()
# jira.getSpecificProjectDetails("10000")
# jira.createNewProject("TAR4", "tarunipm4", "software", "com.pyxis.greenhopper.jira:gh-simplified-scrum-classic", "5c8ff4c490e2362d44935496", "UNASSIGNED")
# jira.getCreateIssueMetadata()
# jira.createIssue("This is my task", "10006", "10002")
# jira.getIssue("TAR3-2")
# jira.deleteIssue("TAR3-4")
# jira.assignIssue("TAR3-5", "5c8ff4c490e2362d44935496")
jira.deleteProject("TAR4")
# jira.getTransitions("10017")
# jira.issueTransition("TAR3-2", "11")