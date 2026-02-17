#This is the main wikipedia we will use
import wikipediaapi
#This API is just for finding related searches in case the wikipedia
#page the user enters doesn't exisit
import wikipedia
#This is the website backend api
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

user = wikipediaapi.Wikipedia(user_agent='EITB2 (aryand4120@gmail.com)', language='en')

userinput = input("Enter a wikipedia page: ")
startpage = user.page(userinput)

if startpage.exists() == True:
    print("It exists!")
    print(startpage.fullurl)
    links = startpage.links
    for title in sorted(links.keys()):
        if title == "Tuberculosis":
            print("It is related to tuberculosis by 1 step!")
            break
else:
    print("Page not found")
    print(wikipedia.search(str(userinput)))

