#This is the main wikipedia we will use
import wikipediaapi
#This API is just for finding related searches in case the wikipedia
#page the user enters doesn't exisit
import wikipedia
#This is the website backend api
from flask import Flask, render_template, request

#This is the library for the graph visual
from dash import Dash, html
import dash_cytoscape as cyto

# Initialize Wikipedia API
user = wikipediaapi.Wikipedia(user_agent='EITB2 (aryand4120@gmail.com)', language='en')

# 1. Setup Flask first
server = Flask(__name__)

# 2. Setup Dash and attach it to the Flask server
# The graph will be viewable at /graph/
app = Dash(__name__, server=server, url_base_pathname='/graph/')

# 3. Define the Dash Layout
app.layout = html.Div([
    html.P("Dash Cytoscape:"),
    cyto.Cytoscape(
        id='cytoscape',
        elements=[
            {'data': {'id': 'ca', 'label': 'Canada'}},
            {'data': {'id': 'on', 'label': 'Ontario'}},
            {'data': {'id': 'qc', 'label': 'Quebec'}},
            {'data': {'id': 'e1', 'source': 'ca', 'target': 'on'}},
            {'data': {'id': 'e2', 'source': 'ca', 'target': 'qc'}}
        ],
        layout={'name': 'breadthfirst'},
        style={'width': '100%', 'height': '500px'}
    )
])

@server.route('/', methods=['GET', 'POST'])
def home():
    result = None
    suggestions = None
    url = None
    message = None

    if request.method == 'POST':
        user_query = request.form.get('wiki_page')

        if user_query:
            page = user.page(user_query)
            if page.exists() == True:
                url = page.fullurl
                print(url)
                message = "Page found!"
            else:
                message = "Page not found"
                suggestions = wikipedia.search(str(user_query))

    return render_template('index.html', message=message, url=url, suggestions=suggestions)

if __name__ == '__main__':
    # Use server.run to start the combined Flask/Dash app
    server.run(debug=True)