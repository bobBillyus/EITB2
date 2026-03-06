import threading
import wikipediaapi
import wikipedia
from dash import Dash, html, dcc, Input, Output, State
import dash_cytoscape as cyto

# 1. Global State
data_lock = threading.Lock()
graph_data = {
    "elements": [],
    "is_searching": False,
    "target": "Tuberculosis"
}

app = Dash(__name__)

# 2. The Layout (Replaces your HTML file)
app.layout = html.Div([
    html.H1("Wikipedia Path Finder"),
    
    # Search Section
    html.Div([
        dcc.Input(id='search-input', type='text', placeholder='Start page...', autocomplete='off'),
        html.Button('Find Path', id='search-btn', n_clicks=0),
        html.Ul(id='suggestions-list', style={'listStyle': 'none', 'padding': 0})
    ]),

    # The Graph
    cyto.Cytoscape(
        id='cytoscape-graph',
        layout={'name': 'breadthfirst'},
        style={'width': '100%', 'height': '600px'},
        elements=[]
    ),

    # The "Pulse" (checks for updates every 1 second)
    dcc.Interval(id='graph-update-timer', interval=1000)
])
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
