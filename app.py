#Apis and Libraries
import wikipediaapi #This is the main wikipedia api we will use
import wikipedia #This API is just for the suggestions in the search bar
from flask import Flask, render_template, request, redirect, jsonify #This is the website backend api
from dash import Dash, html, dcc, Input, Output, no_update, clientside_callback #This is the library for the graph visual
import dash_cytoscape as cyto
import requests #These help grab the links from the wikipedia page
from bs4 import BeautifulSoup
from urllib.parse import unquote #This makes it so it can read special characters
from functools import lru_cache

#Initialize Wikipedia API
user = wikipediaapi.Wikipedia(user_agent='EITB2 (aryand4120@gmail.com)', language='en')

#Flask constructor
server = Flask(__name__)   

@lru_cache(maxsize=100)
def get_wiki_suggestions(query):
    try:
        return wikipedia.search(query, results=5)
    except:
        return []

@server.route('/', methods =["GET", "POST"])
def home():
    if request.method == "POST":
        userinput = request.form.get("wiki_page", "") 
        if userinput:
            return redirect(f'/graph/?page={userinput}')
    return render_template("index.html")

#Suggestions in search bar
@server.route('/live-search', methods=["POST"])
def live_search():
    data = request.get_json() or {}
    query = data.get("query", "").strip()
    if len(query) < 3:
        return jsonify([])
    
    search_options = get_wiki_suggestions(query)
    return jsonify(search_options)

#Setup Dash
app = Dash(__name__, server=server, url_base_pathname='/graph/')

#Empty div
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='graph-content', children="Graph will load here...")
])

if __name__=='__main__':
   server.run(debug=True)

# def get_main_body_links(page_title):
#     print(page_title)
#     formatted_title = page_title.replace(" ", "_")
#     url = f"https://en.wikipedia.org/wiki/{formatted_title}"
    
#     headers = {'User-Agent': 'Link find test(aryand4120@gmail.com)'}

#     response = requests.get(url, headers=headers)
#     if response.status_code != 200:
#         print(f"Error: Could not find page. Status code: {response.status_code}")
#         return []

#     soup = BeautifulSoup(response.content, 'html.parser')
#     content = soup.find(id="mw-content-text").find(class_="mw-parser-output")
    
#     if not content:
#         return []

#     body_links = []
#     stop_ids = {'Notes', 'References', 'External_links', 'See_also', 'Further_reading'}

#     # Iterate through the elements in the main body
#     for element in content.children:
#         # Stop if we hit a bottom-page header
#         if element.name in ['h2', 'h3']:
#             headline = element.find(class_="mw-headline")
#             if headline and headline.get('id') in stop_ids:
#                 break
        
#         # Grab links from paragraphs and lists
#         if element.name in ['p', 'ul', 'ol']:
#             for a_tag in element.find_all('a', href=True):
#                 href = a_tag['href']
#                 # Ensure it's an internal wiki link and not a file/meta-page
#                 if href.startswith('/wiki/') and ':' not in href:
#                     # Clean the URL and handle special characters (like %C5%BE -> ž)
#                     raw_title = href.replace('/wiki/', '').replace('_', ' ')
#                     clean_title = unquote(raw_title)
#                     body_links.append(clean_title)

#     # Use a list comprehension to remove duplicates while keeping order
#     seen = set()
#     return [x for x in body_links if not (x in seen or seen.add(x))]

# # Test it out
# links = get_main_body_links("Torrence Parsons")
# print(links)





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
