import threading
import wikipediaapi
import wikipedia
import dash
from dash import Dash, html, dcc, Input, Output, State, ALL, callback_context, clientside_callback
import dash_cytoscape as cyto

user_agent = 'EITB2 (aryand4120@gmail.com)'
wiki_api = wikipediaapi.Wikipedia(user_agent=user_agent, language='en')

data_lock = threading.Lock()
state = {
    "elements": [],
    "searching": False,
    "found": False,
    "start_node": ""
}

external_stylesheets = [
    'https://cdn.jsdelivr.net/npm/@fontsource/cascadia-mono/index.min.css',
    'https://fonts.googleapis.com/icon?family=Material+Icons',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css',
]

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(className="wrapper", children=[
    # 1. Sidebar
    html.Div([
        html.H2("About EITB2"),
        html.P("Shortest path to Tuberculosis."),
        html.Hr(),
        html.Div(id='status-indicator', children="Waiting...")
    ], id='sidebar', className='sidebar'),

    # 2. Main Area
    html.Div(className="main", id="main-content", children=[
        html.Button(
            html.I(className="material-icons", id="toggle-icon", children="double_arrow"),
            id='sidebar-toggle',
            className='sidebar_toggle_btn',
            n_clicks=0
        ),
        
        html.H1("EITB2: Wikipedia Path Finder"),
        
        html.Div(className="search_box", children=[
            html.Div(className="row", children=[
                dcc.Input(id='search-input', type='text', placeholder='Search Wikipedia...', autoComplete="off"),
                html.Button(html.I(className="fa-solid fa-magnifying-glass"), id='search-btn')
            ]),
            html.Div(id='suggestions-container', className="suggestions_container")
        ]),

        cyto.Cytoscape(
            id='cytoscape-graph',
            layout={'name': 'breadthfirst'},
            style={'width': '100%', 'height': '600px'},
            elements=[]
        ),
        dcc.Interval(id='interval-component', interval=1000)
    ])
])

# --- BACKGROUND LOGIC ---
def find_paths(start_title):
    global state
    target = "Tuberculosis"
    page = wiki_api.page(start_title)
    if not page.exists(): return
    with data_lock:
        state["elements"].append({'data': {'id': start_title, 'label': start_title}})
    links = page.links
    for title in sorted(links.keys()):
        if len(state["elements"]) > 150: break 
        with data_lock:
            state["elements"].append({'data': {'id': title, 'label': title}})
            state["elements"].append({'data': {'source': start_title, 'target': title}})
        if title == target:
            state["found"] = True
            break

# --- CALLBACKS ---

clientside_callback(
    """
    function(n_clicks) {
        const sidebar = document.getElementById('sidebar');
        const icon = document.getElementById('toggle-icon');
        
        if (n_clicks % 2 !== 0) {
            sidebar.classList.add('hidden');
            icon.style.transform = 'rotate(0deg)'; // Points <<
        } else {
            sidebar.classList.remove('hidden');
            icon.style.transform = 'rotate(180deg)'; // Points >>
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output('sidebar-toggle', 'id'),
    Input('sidebar-toggle', 'n_clicks'),
)

@app.callback(
    Output('suggestions-container', 'children'),
    Input('search-input', 'value')
)
def update_suggestions(val):
    if not val or len(val) < 3: return []
    options = wikipedia.search(val, results=5)
    return html.Ul([
        html.Li(html.Button(opt, id={'type': 'suggest-item', 'index': opt})) 
        for opt in options
    ])

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
            state["elements"] = []
            state["start_node"] = start_val
        thread = threading.Thread(target=find_paths, args=(start_val,))
        thread.start()
        return True
    return False

@app.callback(
    Output('cytoscape-graph', 'elements'),
    Input('interval-component', 'n_intervals')
)
def update_graph_live(n):
    with data_lock:
        return list(state["elements"])

if __name__ == '__main__':
    app.run(debug=True)