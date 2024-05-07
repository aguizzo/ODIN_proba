import json
import requests

API_URL='http://localhost:8080'


def get_projects():
    response = requests.get(url=API_URL + '/projects')
    print(response.json())

def get_project(project_id:int):
    response = requests.get(url=API_URL + '/project/' + str(project_id))
    print(response.json())

def get_repositories(project_id:int):
    response = requests.get(url=API_URL + '/project/' + str(project_id) + '/repositories')
    print(response.json())
    
# TODO: obtain the graph from the dataset and render it with javascript    
def get_datasets(project_id:int):
    response = requests.get(url=API_URL + '/project/' + str(project_id) + '/datasets')
    print(response.json())

get_datasets(1)