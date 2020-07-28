import requests
from requests.auth import HTTPBasicAuth
import json
import Jira_get_started as jira_start
from MailFiles import send_mail
import Text_to_Speech as speak

class Jira(object):

	base_url = ""
	output = ""
	mail_body = {}
	all_projects = jira_start.getAllProjects() # get all the projects in the jira workspace
	all_users = jira_start.getAllUsers() # get all the users in the jira workspace

	def __init__(self, base_url, user_email, access_token):
		self.base_url = base_url
		self.auth = HTTPBasicAuth(user_email, access_token)

	def getSpecificProjectDetails(self, **args):
		print("I am getting calling in here")
		project_key = args["project key"]
		url = '/rest/api/2/project/'+project_key
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
			print("I am here also")
			print(self.output)
			self.mail_body = {
				"Project name":response["name"],
				"Project ID":response["id"],
				"Project key":response["key"],
				"Project lead name":response["lead"]["displayName"],
				"Project lead ID":response["lead"]["accountId"] 
			}
			send_mail.sendMail(self.mail_body)
		return self.output

	def createNewProject(self, **args):
		url = '/rest/api/2/project'
		project_name = args["project name"]
		lead_name = args["lead name"]
		# print(type(self.all_users))
		# print(self.all_users[lead_name])
		lead_account_id = '5c8ff4c490e2362d44935496'
		project_type_key = "software"
		project_template_key = "com.pyxis.greenhopper.jira:gh-simplified-scrum-classic"
		project_key = project_name[:3].upper() # change it everytime randomly
		assignee_type = "UNASSIGNED"
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
		print(response.status_code)
		if response.status_code != 201:
			self.output = "Request is not valid"
			return self.output
		else:
			response = json.loads(response.text)
			args = {"project key" : project_key}
			print(args)
			self.output = self.getSpecificProjectDetails(**args)
		return self.output

	def deleteProject(self, **args):
		project_key = args["project key"]
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
		return self.output

	def updateProject(self, **args):
		pass

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

	def createIssue(self, **args):
		# for epic, epic name is needed
		# for subtask, there should be a parent id
		# issue types: 10000(epic), 10001(story), 10002(task), 10003(subtask), 10004(bug) 
		summary = args["summary"]
		# project_id = self.all_projects[args["project key"]]["projectId"]
		project_id = args["project id"]
		issue_type = args["issue type"]
		if issue_type.lower() == "epic":
			issue_id = "10000"
		elif issue_type.lower() == "story":
			issue_id = "10001"
		elif issue_type.lower() == "task":
			issue_id = "10002"
		elif issue_type.lower() == "subtask":
			issue_id = "10003"
		elif issue_type.lower() == "bug":
			issue_id = "10004"
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
		return self.output

	def getIssue(self, **args):
		issue_key = args["issue key"]
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
		return self.output

	def deleteIssue(self, **args):
		issue_key = args["issue key"]
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
		return self.output

	def updateIssue(self, **args):
		pass
		
	def assignIssue(self, **args):
		issue_key = args["issue key"]
		# accountId = self.all_users[args["assignee name"]]["accountId"]
		accountId = '5c8ff4c490e2362d44935496'
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
			self.output = "Issue assigned successfully to {person}".format(person=args["assignee name"])
			self.mail_body = {
				"Status" : "Issue assign successfully",
				"Issue key" : issue_key,
				"Assignee" : accountId
			}
			send_mail.sendMail(self.mail_body)
		return self.output

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

	def issueTransition(self, **args):
		issue_key = args["issue key"]
		transition_type = args["transition type"]
		transition = {"to do":"11", "in progress":"21", "done":"31"}
		transition_id = transition[transition_type.lower()]
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
			self.output = "Issue is transit to {type}".format(type=args["transition type"])
			self.mail_body = {
				"Status" : "Issue transition success",
				"Issue key" : issue_key,
				"Transition level" : args["transition type"]
			}
			send_mail.sendMail(self.mail_body)
		return self.output

# jira = Jira()
# jira.getSpecificProjectDetails("10000")
# jira.createNewProject("TAR4", "tarunipm4", "software", "com.pyxis.greenhopper.jira:gh-simplified-scrum-classic", "5c8ff4c490e2362d44935496", "UNASSIGNED")
# jira.getCreateIssueMetadata()
# jira.createIssue("This is my task", "10006", "10002")
# jira.getIssue("TAR3-2")
# jira.deleteIssue("TAR3-4")
# jira.assignIssue("TAR3-5", "5c8ff4c490e2362d44935496")
# jira.deleteProject("TAR4")
# jira.getTransitions("10017")
# jira.issueTransition("TAR3-2", "11")