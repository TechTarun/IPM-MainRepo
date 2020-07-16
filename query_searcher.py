import json
import extract_key as ek
import web_text2speech as t2s
from fuzzywuzzy import process
import ner
import requests
import github_parser as g_parser

def load_data(filepath):
    with open(filepath, "r") as f:
        data = json.load(f)
    f.close()
    return data

def find_intersection(doc_list):
    doc_id = list()
    l = len(doc_list)
    doc_id = set(doc_list[0])
    for i in range(1, l):
        doc_id.intersection_update(set(doc_list[i]))
    return list(doc_id)

def prepare_lookup(data):
    look_up = dict()
    data_length = len(data)
    word_list = list()
    for a in range(data_length):
        word_list = ek.extract(data[a]['title'])
        for word in word_list:
            if word in look_up:
                look_up[word].append(data[a]['doc_id'])
            else:
                look_up[word] = list()
                look_up[word].append(data[a]['doc_id'])
    return(look_up)


def process_owq(look_up, query_word):
    if(query_word in look_up):
        t2s.say("Documents are:- " + look_up[query_word])
    else:
        t2s.say("No APIs found!!")
        return

def process_ftq(look_up, query, repo_list):
    doc_list = list()
    keywords = ek.extract(query)
    for word in keywords:
        if word in look_up:
            doc_list.append(look_up[word])
    if(len(doc_list) == 0):
        t2s.say("Query not recognized!!")


    else:
        doc_id = find_intersection(doc_list)
        if(len(doc_id) == 0):
            t2s.say("Query not so accurate, try the following suggestions...")
            show_suggestions(query)

        elif(len(doc_id) == 1):
            with open("github_data.json", "r") as f:
                data = json.load(f)
            f.close()
            api = data[doc_id[0]-1]['api']
            parameters = ner.main(query)
            repo_list = create_api(api, parameters)
        else:
            with open("github_data.json", "r") as f:
                data = json.load(f)
            f.close()
            choices = list()
            for doc in doc_id:
                choices.append(data[doc-1]['title'])
            right_title = process.extractOne(query, choices)[0]
            for doc in doc_id:
                if(data[doc-1]['title'] == right_title):
                    api = data[doc-1]['api']
            parameters = ner.main(query)
            repo_list = create_api(api, parameters)
    return repo_list


def create_api(api, parameters):
    print(api)
    repo_list = list()
    api_list = api.split('+')
    parameter_req = list()
    final_api = ""
    for item in api_list:
        if item in all_parameter_list:
            parameter_req.append(item)
    if (len(parameter_req) == len(parameters)):
        for item in api_list:
            if (item not in parameter_req):
                final_api += item
            else:
                if (item in ('owner', 'username', 'org')):
                    final_api += parameters['usr']
                elif(item == 'repo'):
                    final_api += parameters['rep']
                elif(item == 'language'):
                    final_api += parameters['lan']
        final_api = filter_api(final_api)
        print(final_api)
        p = requests.get(final_api)
        x = p.json()
        print(x)
        repo_list = g_parser.parse(x)
    else:
        t2s.say("Query is incomplete")
    return repo_list

def filter_api(final_api):
    bad_chars = ["'"]

    # initializing test string
    test_string = final_api

    for i in bad_chars:
        test_string = test_string.replace(i, '')

    return str(test_string)


def show_suggestions(query):
    choice_list = []
    filepath = "sample_query.txt"
    with open(filepath, 'r') as f:
        for line in f:
            choice_list.append(line)
        f.close()
    suggestions = process.extractOne(query, choice_list)
    t2s.say(suggestions[0])


def fetch_parameters(query):
    query_list = query.split()
    if('project' in query):
        repo_pos = query_list.index('project')
        repo = query_list[repo_pos+1]
    if('repository' in query):
        repo_pos = query_list.index('repository')
        repo = query_list[repo_pos+1]
    if('project' in query):
        repo_pos = query_list.index('project')
        repo = query_list[repo_pos+1]


def execute(query):
    repo_list = []
    filepath = "github_data.json"
    data = load_data(filepath)
    look_up = prepare_lookup(data)
    if len(query) == 1:
        process_owq(look_up, query)
    else:
        repo_list = process_ftq(look_up, query, repo_list)
    return repo_list

all_parameter_list = ['username', 'repo', 'org', 'owner',
                      'language', 'branch', 'creator', 'body', 'query']


