from JiraFiles.Jira_api import Jira
from GithubFiles.Github_api import Git
import config_file as config
from InputOutputFiles import Speech_to_Text as listen
from InputOutputFiles import Text_to_Speech as speak


jira = Jira(config.JIRA_BASE_URL, config.JIRA_USER_EMAIL, config.JIRA_ACCESS_TOKEN)
github = Git(config.GITHUB_ACCESS_TOKEN)
args = {}
#bitbucket object
#confluence object
query_type_list ={'create':['create', 'make', 'build', 'built', 'form', 'generate'], 'delete':['delete', 'remove', 'clear', 'erase', 'trash', 'bin'], 'update':['update', 'modify', 'change', 'edit'], 'details':['get', 'fetch', 'show', 'details'], 'transition':['to do', 'in progress', 'done'], 'assign':['assign']}
domain_list = ['repository', 'project', 'user', 'issue' , 'ticket']

#################### query map #####################
QUERY_MAP = {
    "Github" : {
    },

    "Jira" : {
        "create" : {
            "project" : {"function":jira.createNewProject, "args":["project name", "lead name"]},
            "issue" : {"function":jira.createIssue, "args":["summary", "project id", "issue type"]}
        },
        "delete" : {
            "project" : {"function":jira.deleteProject, "args":["project key"]},
            "issue" : {"function":jira.deleteIssue, "args":["issue key"]}
        },
        "update" : {
            "project" : {"function":jira.updateProject, "args":[]},
            "issue" : {"function":jira.updateIssue, "args":[]}
        },
        "details" : {
            "project" : {"function":jira.getSpecificProjectDetails, "args":["project key"]},
            "issue" : {"function":jira.getIssue, "args":["issue key"]}
        },
        "transition" : {
            "issue" : {"function":jira.issueTransition, "args":["issue key", "transition type"]}
        },
        "assign" : {
            "issue" : {"function":jira.assignIssue, "args":["issue key", "assignee name"]}
        }
    },

    "Bitbucket" : {
    },

    "Confluence" : {
    }
} 
################### end query map ####################

################### get query type ##################

def getQueryType(text):
    query_type = ""
    """query type includes create, delete, assign, transition, update, details"""
    for key in query_type_list:
        value = query_type_list[key]
        for word in value:
            if word in text:
                query_type = key
                return query_type


################### end get query type ###############

################### get domain #####################

def getDomain(text):
    """domain includes repository, project, user, issue"""
    domain = ""
    for word in domain_list:
        if word in text:
            domain = word
            if domain == 'ticket':
                domain = 'issue'
            return domain

################### end domain #####################

################# get arguments ################

def getArgs(text, provider, domain, query_type):
    params = {}
    args = QUERY_MAP[provider][query_type][domain]["args"]
    speak.say("Please give required details")
    for arg in args:
        speak.say("What is"+arg)
        params[arg] = listen.listenInput()
    print(params)
    return params

################# end get arguments ###############

################### get APi #################

def getAPIOutput(text, provider):
    domain = getDomain(text)
    query_type = getQueryType(text)
    print(domain)
    print(query_type)
    args = getArgs(text, provider, domain, query_type)  
    output = QUERY_MAP[provider][query_type][domain]["function"](**args)
    return output

################### end get API ###############