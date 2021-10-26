import pymongo
import bcrypt
import requests
import pandas as pd
from bs4 import BeautifulSoup
from flask import Flask,render_template,request,send_file,url_for, redirect, session

app = Flask(__name__)

app.secret_key = 'keynotknown'

client = pymongo.MongoClient(
    "mongodb+srv://whale-crawl:binomo123@cluster0.w1jbe.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

# get the database name
db = client.get_database('clustergr8')
# get the particular collection that contains the data
records = db.users

@app.route('/')
def ho():
    return render_template("/index.html")

@app.route('/',methods=['POST','GET'])
def output():
    
    if request.method == 'POST':
      
        urls = request.form["url"]
        
        grab = requests.get(urls)
        soup = BeautifulSoup(grab.text, 'html.parser')
        
        # # opening a file in write mode
        f = open("new.csv", "w+")
        # traverse paragraphs from soup
        data = """"""
        count = 1
        for link in soup.find_all("a"):
            data = data + f"\n{count} "+link.get('href')
            count = count + 1
            
            # f.write("\n")
            
        
        # f.close()
    return render_template("/index.html", data=data)


@app.route("/submit")
def n():
    return redirect(url_for("/templates/downl.html"))







# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     # if request.method == 'POST':
#     #     email=request.form['email']
#     #     password=request.form['password']
#     #     name=request.form['name']
        
#     #     print(email, password, name)
#     # # return render_template('/index.html',info= email)
#     #     # print(request.form.keys())
#     #     return render_template('/index.html')
@app.route("/signup", methods=['post', 'get'])
def signup():
    print("message",request.form)
    message = 'Signup to your account'
    # if method post in index
    # if "email" in session:
    #     return render_template("/index.html")
    if request.method == "POST":
        name = request.form.get("name")
        
        email = request.form.get("email")
        password1 = request.form.get("password")
       
        # if found in database showcase that it's found
        email_found = records.find_one({"email": email})
        if email_found:
            message = 'This email already exists in database'
            return render_template("createaccount.html", message=message)
  
        else:
            # hash the password and encode it
            hashed = bcrypt.hashpw(password1.encode('utf-8'), bcrypt.gensalt())
            # assing them in a dictionary in key value pairs
            user_input = {'name': name, 'email': email,'password': hashed}
            # insert it in the record collection
            records.insert_one(user_input)

            # find the new created account and its email
            user_data = records.find_one({"email": email})
            new_email = user_data['email']
            # if registered redirect to logged in as the registered user
            session["email"] = new_email
            return render_template("/index.html")
    return render_template("createaccount.html", message=message)

@app.route("/login", methods=["POST", "GET"])
def login():
    
    message = 'Please login to your account'
    # if "email" in session:
    #     return render_template("/index.html")

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # check if email exists in database
        email_found = records.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            # encode the password and check if it matches
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return render_template("/index.html")
            else:
                if "email" in session:
                    return redirect(url_for("logged_in"))
                message = 'Wrong password'
                return render_template("createaccount.html", message=message)
        else:
            message = 'Email not found'
            return render_template("createaccount.html", message=message)
    return render_template("createaccount.html", message=message)


@app.route('/download')    
def download_file():
    path="urlfile.csv"
    return send_file(path, as_attachment=True)

@app.route("/createaccount")
def createaccount():
    return render_template('createaccount.html')  
    

if __name__ == "__main__":
    app.run(debug=True)