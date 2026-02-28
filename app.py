#This is the main wikipedia api we will use
import wikipediaapi
#This API is just for finding related searches in case the wikipedia page the user enters doesn't exisit
import wikipedia
#This is the website backend api
from flask import Flask, render_template, request
#This is the library for the graph visual
from dash import Dash, html, dcc, Input, Output, no_update, clientside_callback
import dash_cytoscape as cyto

#Initialize Wikipedia API
user = wikipediaapi.Wikipedia(user_agent='EITB2 (aryand4120@gmail.com)', language='en')

#Flask constructor
app = Flask(__name__)   

@app.route('/', methods =["GET", "POST"])
def gfg():
    if request.method == "POST":
       userinput = request.form.get("fname")
       srcpage = user.page(userinput)
    return render_template("index.html", result=srcpage)

if __name__=='__main__':
   app.run()

# #Setup Flask 
# server = Flask(__name__)

# @server.route('/', methods=['GET', 'POST'])
# def home():
#     result = None
#     suggestions = None
#     query_for_graph = "" # This will be passed to the iframe

#     if request.method == 'POST':
#         user_query = request.form.get('wiki_page')

#         if user_query:
#             page = user.page(user_query)
#             if page.exists() == True:
#                 query_for_graph = user_query # Set this to update the iframe
#                 result = {'title': page.title}
#             else:
#                 suggestions = wikipedia.search(user_query)

#     return render_template('index.html', suggestions=suggestions, result=result, query=query_for_graph)

# # 2. Setup Dash
# app = Dash(__name__, server=server, url_base_pathname='/graph/')

# #Empty div
# app.layout = html.Div([
#     dcc.Location(id='url', refresh=False),
#     html.Div(id='graph-content')
# ])

# # 4. The Callback: This builds the graph ONLY after the URL changes
# @app.callback(
#     Output('graph-content', 'children'),
#     Input('url', 'search') # This watches the "?name=..." part of the URL
# )
# def update_graph(search):
#     if not search:
#         return html.P("Search for a page to generate the graph.")
    
#     # Extract the page name from the URL (?name=PageName)
#     page_name = search.split('=')[-1].replace('%20', ' ')
#     page = user.page(page_name)
    
#     if not page.exists():
#         return html.P("Page data not available for graph.")

#     # NOW we create the elements dynamically
#     return cyto.Cytoscape(
#         id='cytoscape',
#         elements=[
#             {'data': {'id': 'srcpage', 'label': page.title,'url': page.fullurl}},
#             {'data': {'id': 'on', 'label': 'Ontario'}},
#             {'data': {'id': 'e1', 'source': 'srcpage', 'target': 'on'}},
#         ],
#         layout={'name': 'breadthfirst'},
#         style={'width': '100%', 'height': '500px'}
#     )

# if __name__ == '__main__':
#     server.run(debug=True)