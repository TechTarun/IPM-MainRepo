import requests
import requests
from requests.auth import HTTPBasicAuth
import json
import Jira_get_started as jira

class Jira(object):

	base_url = "https://abesit-ipm.atlassian.net"
	auth = HTTPBasicAuth("tarunagarwal27.99@gmail.com", "tl4F0d5aapRqiR7BfGkiBBDD")
	all_projects = jira.getAllProjects() # get all the projects in the jira workspace
	all_users = jira.getAllUsers() # get all the users in the jira workspace

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
		print(response.text)

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
		print(response)
		print(response.text)

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
		print(response)
		print(response.text)

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
		print(response)
		print(response.text)

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
		print(response)
		print(response.text)

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
		print(response)
		print(response.text)

jira = Jira()
# jira.getSpecificProjectDetails("10000")
# jira.createNewProject("TAR2", "tarunipm2", "software", "com.pyxis.greenhopper.jira:gh-simplified-scrum-classic", "5c8ff4c490e2362d44935496", "UNASSIGNED")
# jira.getCreateIssueMetadata()
# jira.createIssue("This is default summary", "10004", "10002")
# jira.getIssue("IPM-3")
# jira.deleteIssue("10011")
# jira.assignIssue("10017", "5c8ff4c490e2362d44935496")