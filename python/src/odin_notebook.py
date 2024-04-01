import json
from html_builder import build_html
from IPython.display import display, HTML
import requests

SERVER_URL='http://localhost:3000'

class OdinNotebook:

    def __init__(self):
        self.context = "notebook"

    
    def draw_plot(self, data):
        # Convert data to JSON
        json_data = self.data_to_json(data)
        # Pass the JSON data to html builder
        html = build_html(json_data)

        display(html, raw=True)


    def data_to_json(self, data):
        nodes = []
        links = []
        for i in range(len(data)):
            node = {'name': i}
            nodes.append(node)
            for vertex in data[i]:
                edge = {'source': i, 'target': vertex}
                links.append(edge)
        graph = {
            'nodes': nodes,
            'links': links
        }
        return "'"+json.dumps(graph)+"'"
    
    def request_demo(self):
        response = requests.get(url="http://localhost:3000/request")
        print(response)
        print(response.json())