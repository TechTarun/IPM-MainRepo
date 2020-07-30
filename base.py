from JiraFiles.Jira_api import Jira
from GithubFiles.Github_api import Git
import config_file as config
from InputOutputFiles import Speech_to_Text as listen
from InputOutputFiles import Text_to_Speech as speak
from InputOutputFiles import Process_input as process


jira = Jira(config.JIRA_BASE_URL, config.JIRA_USER_EMAIL, config.JIRA_ACCESS_TOKEN)
github = Git(config.GITHUB_ACCESS_TOKEN)
args = {}
#bitbucket object
#confluence object
jira_query_type_list = {'create':['create', 'make', 'build', 'built', 'form', 'generate', 'add'], 'delete':['delete', 'remove', 'clear', 'erase', 'trash', 'bin'], 'update':['update', 'modify', 'change', 'edit'], 'details':['get', 'fetch', 'show', 'details'], 'transition':['to do', 'in progress', 'done'], 'assign':['assign']}
jira_domain_list = ['project', 'user', 'issue' , 'ticket']


github_query_type_list = {'create':['create', 'make', 'form', 'add'], 'close':['close', 'end'], 'delete':['delete', 'remove'], 'search':['search', 'find'], 'details':['show', 'detail', 'get', 'fetch']}
github_domain_list = ['repository', 'file', 'issue', 'commit']
github_subdomain_list = ['body', 'label', 'number', 'latest', 'good first issue', 'language', 'open']

query_type_list_dict = {"Jira":jira_query_type_list, "Github":github_query_type_list}
domain_list_dict = {"Jira":jira_domain_list, "Github":github_domain_list}
subdomain_list_dict = {"Github":github_subdomain_list}

#################### query map #####################
QUERY_MAP = {
    "Github" : {
        "create" : {
            "repository" : {
                None : {"function":github.createNewRepo, "args":["repo name"]}
            },
            "file" : {
                None : {"function":github.createNewFileInRepo, "args":["repo name", "file name"]}
            },
            "issue" : {
                None : {"function":github.createNewIssue, "args":["repo name", "title"]},
                "body" : {"function":github.createIssueWithBody, "args":["repo name", "title", "body description"]},
                "label" : {"function":github.createIssueWithLabel, "args":["repo name", "title", "label"]}
            }
        },
        "close" : {
            "issue" : {
                "open" : {"function":github.closeAllOpenIssues, "args":["repo name"]},
                "number" : {"function":github.closeIssueByNumber, "args":["repo name", "issue number"]},
                None : {"function":github.closeIssueByNumber, "args":["repo name", "issue number"]}
            }
        },
        "delete" : {
            "file" : {
                None : {"function":github.deleteFileFromRepo, "args":["repo name", "file name"]}
            }
        },
        "search" : {
            "repository" : {
                "good first issue" : {"function":github.searchRepoWithGoodFirstIssue, "args":[]}
            },
            "repository" : {
                "language" : {"function":github.searchRepoByLanguage, "args":["language"]}
            }
        },
        "details" : {
            "issue" : {
                "open" : {"function":github.listOfOpenIssues, "args":["repo name"]},
                None : {"function":github.getIssueByNumber, "args":["repo name", "issue number"]}
            },
            "repository" : {
                "label" : {"function":github.getLabelsOfRepo, "args":["repo name"]},
                None : {"function":github.getAllContentsOfRepo, "args":["repo name"]}
            },
            "commit" : {
                "latest" : {"function":github.getLatestCommitDateOfUser, "args":[]}
            }
        }
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

def getQueryType(text, provider):
    query_type_list = query_type_list_dict[provider]
    query_type = ""
    """query type includes create, delete, assign, transition, update, details"""
    for key in query_type_list:
        value = query_type_list[key]
        for word in value:
            if word == text.split()[0]:
                query_type = key
                return query_type


################### end get query type ###############

################### get domain #####################

def getDomain(text, provider):
    """domain includes repository, project, user, issue"""
    domain_list = domain_list_dict[provider]
    domain = ""
    for word in domain_list:
        if word in text:
            domain = word
            if domain == 'ticket':
                domain = 'issue'
            return domain

################### end domain #####################

################### get sub domain #####################

def getSubDomain(text, provider):
    """domain includes repository, project, user, issue"""
    subdomain_list = subdomain_list_dict[provider]
    subdomain = None
    for word in subdomain_list:
        if word in text:
            subdomain = word
            return subdomain

################### end sub domain #####################

################# get arguments ################

def getArgs(text, provider, query_type, domain, subdomain=None):
    params = {}
    if provider not in ['Github', 'Bitbucket']:
        args = QUERY_MAP[provider][query_type][domain]["args"]
    else:
        args = QUERY_MAP[provider][query_type][domain][subdomain]["args"]
    if len(args) == 0:
        return params
    speak.say("Please give required details")
    for arg in args:
        speak.say("What is"+arg)
        params[arg] = listen.listenInput()
        if arg == "file name":
            params[arg] = process.createFileName(params[arg])
    print(params)
    return params

################# end get arguments ###############

################### get APi #################

def getAPIOutput(text, provider):
    text = process.extractRootwords(text)
    domain = getDomain(text, provider)
    query_type = getQueryType(text, provider)
    subdomain = None
    if provider in ['Github', 'Bitbucket']:
        subdomain = getSubDomain(text, provider)
    print(query_type)
    print(domain)
    print(subdomain)
    args = getArgs(text, provider, query_type, domain, subdomain)
    if provider not in ['Github', 'Bitbucket']:
        output = QUERY_MAP[provider][query_type][domain]["function"](**args)
    else:
        output = QUERY_MAP[provider][query_type][domain][subdomain]["function"](**args)
    return output

################### end get API ###############