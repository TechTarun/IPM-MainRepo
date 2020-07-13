import json

def parse(data):
    index = 0
    while(True):
        repo_details = dict()
        try:
            # print(data[index]['name'])
            if('name' in data[index].keys()):
                print(data[index]['name'])
                repo_details['branch_name'] = data[index]['name']
            if('full_name' in data[index].keys()):
                repo_details['full_name'] = data[index]['full_name']
            else:
                repo_details['full_name'] = data[index]['login']
            repo_details['repo_url'] = data[index]['html_url']
            if('description' in data[index].keys()):
                repo_details['description'] = data[index]['description']
            if('contributions' in data[index]):
                repo_details['contributions'] = data[index]['contributions']
            repo_list.append(repo_details)
            index += 1
        except:
            break
    return repo_list

# def parse_user_details(data):
#     index = 0
#     while(True):
#         repo_details = dict()
#         try:
#             repo_details['full_name'] = data[index]['login']
#             repo_details['id_url'] = data[index]['html_url']
#             repo_details['contributions'] = data[index]['contributions']
#             repo_list.append(repo_details)
#             index += 1
#         except:
#             break
#     return repo_list

repo_list = list()