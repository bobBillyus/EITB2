#This is the main wikipedia we will use
import wikipediaapi
#This API is just for finding related searches in case the wikipedia
#page the user enters doesn't exisit
import wikipedia
#This is the website backend api
from flask import Flask, render_template, request

#This is the library for the graph visual
from dash import Dash, html, dcc, Input, Output
import dash_cytoscape as cyto

#Initialize Wikipedia API
user = wikipediaapi.Wikipedia(user_agent='EITB2 (aryand4120@gmail.com)', language='en')

#Setup Flask 
server = Flask(__name__)

@server.route('/', methods=['GET', 'POST'])
def home():
    result = None
    suggestions = None
    url = None
    query_for_graph = "" # This will be passed to the iframe

    if request.method == 'POST':
        user_query = request.form.get('wiki_page')

        if user_query:
            page = user.page(user_query)
            if page.exists() == True:
                url = page.fullurl
                query_for_graph = user_query # Set this to update the iframe
                result = {'title': page.title, 'summary': page.summary[:500]}
            else:
                suggestions = wikipedia.search(str(user_query))

    return render_template('index.html', url=url, suggestions=suggestions, result=result, query=query_for_graph)

# 2. Setup Dash
app = Dash(__name__, server=server, url_base_pathname='/graph/')

# 3. Define a "Loading" Layout
# We start with an empty Div and a Location component to watch the URL
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='graph-content')
])

# 4. The Callback: This builds the graph ONLY after the URL changes
@app.callback(
    Output('graph-content', 'children'),
    Input('url', 'search') # This watches the "?name=..." part of the URL
)
def update_graph(search):
    if not search:
        return html.P("Search for a page to generate the graph.")
    
    # Extract the page name from the URL (?name=PageName)
    page_name = search.split('=')[-1].replace('%20', ' ')
    page = user.page(page_name)
    
    if not page.exists():
        return html.P("Page data not available for graph.")

    # NOW we create the elements dynamically
    return cyto.Cytoscape(
        id='cytoscape',
        elements=[
            {'data': {'id': 'target', 'label': page.title}},
            {'data': {'id': 'on', 'label': 'Ontario'}},
            {'data': {'id': 'e1', 'source': 'target', 'target': 'on'}},
        ],
        layout={'name': 'breadthfirst'},
        style={'width': '100%', 'height': '500px'}
    )

if __name__ == '__main__':
    server.run(debug=True)