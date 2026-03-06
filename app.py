import threading
import wikipediaapi
import wikipedia
import dash
from dash import Dash, html, dcc, Input, Output, State, ALL, callback_context
import dash_cytoscape as cyto

# 1. SETUP & GLOBAL DATA
user_agent = 'EITB2 (aryand4120@gmail.com)'
wiki_api = wikipediaapi.Wikipedia(user_agent=user_agent, language='en')

data_lock = threading.Lock()
# This dictionary is the "brain" shared by the crawler and the website
state = {
    "elements": [],
    "searching": False,
    "found": False,
    "start_node": ""
}

app = Dash(__name__)

# 2. LAYOUT (No more index.html needed!)
app.layout = html.Div([
    # 1. The Sidebar
    html.Div([
        html.H2("About EITB2"),
        html.P("This tool finds the shortest path between any Wikipedia page and Tuberculosis."),
        html.Hr(),
        html.P("Status:"),
        html.Div(id='status-indicator', children="Waiting for search...")
    ], id='sidebar', style={
        'position': 'fixed', 'top': 0, 'left': 0, 'bottom': 0,
        'width': '250px', 'padding': '20px', 'backgroundColor': '#f8f9fa',
        'borderRight': '1px solid #ddd', 'zIndex': 100
    }),

    # 2. Main Content Area (Shifted to the right to make room for sidebar)
    html.Div([
        html.H1("EITB2: Wikipedia Path Finder"),
        
        # Search Box
        html.Div([
            dcc.Input(id='search-input', type='text', placeholder='Search Wikipedia...'),
            html.Button('Search', id='search-btn', n_clicks=0),
            html.Div(id='suggestions-container')
        ], style={'marginBottom': '30px'}),

        # The Graph
        cyto.Cytoscape(
            id='cytoscape-graph',
            layout={'name': 'breadthfirst'},
            style={'width': '100%', 'height': '600px'},
            elements=[]
        ),
        
        dcc.Interval(id='interval-component', interval=1000)
    ], style={'marginLeft': '270px', 'padding': '20px'}) # This marginLeft is the key!
])

def find_paths(start_title):
    global state
    target = "Tuberculosis"
    
    page = wiki_api.page(start_title)
    if not page.exists(): return

    # 1. Add the starting node
    with data_lock:
        state["elements"].append({'data': {'id': start_title, 'label': start_title}})

    # 2. Get links and add them to the graph
    links = page.links
    for title in sorted(links.keys()):
        # Limit to avoid hitting API rate limits or crashing the browser
        if len(state["elements"]) > 150: 
            break 
        
        with data_lock:
            # Add the new node
            state["elements"].append({'data': {'id': title, 'label': title}})
            # Add the edge from start_title to this new title
            state["elements"].append({'data': {'source': start_title, 'target': title}})
        
        if title == target:
            state["found"] = True
            print("Found Tuberculosis!")
            break

# 4. CALLBACKS (Replacing your JS and Flask Routes)

# Callback: Autocomplete Suggestions
@app.callback(
    Output('suggestions-container', 'children'),
    Input('search-input', 'value')
)
def update_suggestions(val):
    if not val or len(val) < 3: return []
    options = wikipedia.search(val, results=5)
    return html.Ul([
        html.Li(html.Button(opt, id={'type': 'suggest-item', 'index': opt}, 
                style={'width': '300px', 'textAlign': 'left'})) 
        for opt in options
    ], style={'listStyle': 'none', 'padding': 0, 'background': 'white', 'border': '1px solid #ddd'})

# Callback: Start Search when Button Clicked
@app.callback(
    Output('search-btn', 'disabled'),
    Input('search-btn', 'n_clicks'),
    State('search-input', 'value'),
    prevent_initial_call=True
)
def start_search(n, start_val):
    if n > 0 and start_val:
        global state
        with data_lock:
            state["elements"] = [] # Reset graph
            state["start_node"] = start_val
        
        # Start the background thread
        thread = threading.Thread(target=find_paths, args=(start_val,))
        thread.start()
        return True
    return False

# Callback: Update Graph Visuals Every Second
@app.callback(
    Output('cytoscape-graph', 'elements'),
    Input('interval-component', 'n_intervals')
)
def update_graph_live(n):
    with data_lock:
        return list(state["elements"])

if __name__ == '__main__':
    app.run(debug=True)