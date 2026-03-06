#Apis and Libraries
import wikipediaapi #This is the main wikipedia api we will use
import wikipedia #This API is just for the suggestions in the search bar
from flask import Flask, render_template, request, redirect, jsonify #This is the website backend api
from dash import Dash, html, dcc, Input, Output, no_update, clientside_callback #This is the library for the graph visual
import dash_cytoscape as cyto
import requests #These help grab the links from the wikipedia page
from bs4 import BeautifulSoup
from urllib.parse import unquote #This makes it so it can read special characters

#Initialize Wikipedia API
user = wikipediaapi.Wikipedia(user_agent='EITB2 (aryand4120@gmail.com)', language='en')

#Flask constructor
server = Flask(__name__)   

@server.route('/', methods =["GET", "POST"])
def home():
    if request.method == "POST":
        query = request.form.get("searchbar")
        print(f"User searched for: {query}")
        
    return render_template("index.html")

#Suggestions in search bar
@server.route('/autocomplete', methods=["POST"])
def live_search():
    data = request.get_json()
    query = data.get("query", "")
    search_options = wikipedia.search(query, results=5) 
    return jsonify(search_options)


#Setup Dash
app = Dash(__name__, server=server, url_base_pathname='/graph/')

#Empty div
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='graph-content')
])


if __name__=='__main__':
   server.run(debug=True)