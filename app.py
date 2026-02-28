#This is the main wikipedia we will use
import wikipediaapi
#This API is just for finding related searches in case the wikipedia
#page the user enters doesn't exisit
import wikipedia
#This is the website backend api
from flask import Flask, render_template, request

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
        print('ok')
        if page.exists():
            url = page.fullurl
            message = "Page found!"

    return render_template('index.html', message=message, url=url, suggestions=suggestions)

if __name__ == '__main__':
    app.run(debug=True)


# userinput = input("Enter a wikipedia page: ")
# startpage = user.page(userinput)

# if startpage.exists() == True:
#     print("It exists!")
#     print(startpage.fullurl)
#     links = startpage.links
#     for title in sorted(links.keys()):
#         if title == "Tuberculosis":
#             print("It is related to tuberculosis by 1 step!")
#             break
# else:
#     print("Page not found")
#     print(wikipedia.search(str(userinput)))

# import wikipediaapi
# import wikipedia
# from flask import Flask, render_template, request

# app = Flask(__name__)

# # Initialize the Wikipedia API outside the route
# wiki_api = wikipediaapi.Wikipedia(user_agent='EITB2 (aryand4120@gmail.com)', language='en')

# @app.route('/', methods=['GET', 'POST'])
# def home():
#     result = None
#     suggestions = None
#     url = None
#     message = None

#     if request.method == 'POST':
#         # 1. Get the data from the HTML input (name="wiki_page")
#         user_query = request.form.get('wiki_page')

#         if user_query:
#             # 2. Check if the page exists
#             page = wiki_api.page(user_query)

#             if page.exists():
#                 url = page.fullurl
#                 message = "Page found!"
                
#                 # Check for the Tuberculosis link logic
#                 links = page.links
#                 if "Tuberculosis" in links:
#                     message = "It is related to Tuberculosis by 1 step!"
#             else:
#                 message = "Page not found."
#                 # 3. Get suggestions using the other library
#                 suggestions = wikipedia.search(user_query)

#     # 4. Pass all variables back to your index.html
#     return render_template('index.html', 
#                            message=message, 
#                            url=url, 
#                            suggestions=suggestions)

# if __name__ == '__main__':
#     app.run(debug=True)