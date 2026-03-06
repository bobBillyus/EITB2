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
    html.H1("Wikipedia Path to Tuberculosis", style={'textAlign': 'center', 'fontFamily': 'Cascadia Mono'}),
    
    html.Div([
        dcc.Input(id='search-input', type='text', placeholder='Enter a starting page...', 
                  style={'width': '300px', 'padding': '10px'}),
        html.Button('Search', id='search-btn', n_clicks=0, style={'padding': '10px'}),
        html.Div(id='suggestions-container', style={'position': 'absolute', 'zIndex': '1000'})
    ], style={'textAlign': 'center', 'marginBottom': '20px'}),

    # The Graph Display
    cyto.Cytoscape(
        id='cytoscape-graph',
        layout={'name': 'breadthfirst'},
        style={'width': '100%', 'height': '600px', 'border': '1px solid #ccc'},
        elements=[],
        stylesheet=[
            {'selector': 'node', 'style': {'content': 'data(label)', 'background-color': '#0074D9', 'color': 'white'}},
            {'selector': '[id = "Tuberculosis"]', 'style': {'background-color': 'red', 'shape': 'diamond'}},
            {'selector': 'edge', 'style': {'line-color': '#999', 'width': 2, 'curve-style': 'bezier'}}
        ]
    ),

    # The Heartbeat (checks for new data every 1 second)
    dcc.Interval(id='interval-component', interval=1000, n_intervals=0)
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
    app.run_server(debug=True)