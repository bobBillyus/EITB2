#This is the main wikipedia we will use
import wikipediaapi
#This API is just for finding related searches in case the wikipedia
#page the user enters doesn't exisit
import wikipedia
#This is the website backend api
from flask import Flask, render_template, request

#This is the library for the graph visual
import plotly.graph_objects as go
import networkx as nx

user = wikipediaapi.Wikipedia(user_agent='EITB2 (aryand4120@gmail.com)', language='en')

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
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

    return render_template('index.html', message=message, url=url, suggestions=suggestions)

if __name__ == '__main__':
    app.run(debug=True)