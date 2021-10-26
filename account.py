from flask import Flask, render_template, request, url_for, redirect, session
import pymongo
import bcrypt
import requests

app = Flask(__name__)
app.secret_key = 'keynotknown'

client = pymongo.MongoClient(
    "mongodb+srv://whale-crawl:binomo123@clustergr8.w1jbe.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

# get the database name
db = client.get_database('clustergr8')
# get the particular collection that contains the data
records = db.users


# @app.route('/', methods=["POST", "GET"])
# def index():
#     if request.method == "GET":
#         return redirect(url_for("dashboard"))
#     return redirect(url_for("login"))

# @app.route('/manasjr/manasjr10', methods=["POST", "GET"])
# def adminroute():
#     if request.method == "GET":
#         user_data = records.find({})
#         return render_template("admin.html", user_data=user_data)
#     return redirect(url_for("login"))




# @app.route('/dashboard')
# def dashboard():
#     if "email" in session:
#         s = requests.Session()
#         p = s.post("https://n00btrader.com/signal/app.system/api/auth", data={
#             "username": 'deepuprajapti5@gmail.com',
#             "password": "binomo123"
#         })
#         data = p.json()
#         session['token'] = data['data']['token']
#         email = session["email"]
#         user_data = records.find_one({"email": email})
#         # if registered redirect to logged in as the registered user
#         if user_data is None:
#             session.pop("email", None)
#             return redirect(url_for("login"))
#         return render_template("dashboard.html", user_data=user_data)
#     return redirect(url_for("login"))


@app.route("/login", methods=["POST", "GET"])
def login():
    message = 'Please login to your account'
    if "email" in session:
        return redirect(url_for("dashboard"))

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
                return redirect(url_for("dashboard"))
            else:
                if "email" in session:
                    return redirect(url_for("logged_in"))
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'Email not found'
            return render_template('login.html', message=message)
    return render_template('login.html', message=message)


@app.route("/signup", methods=['post', 'get'])
def signup():
    message = 'Signup to your account'
    # if method post in index
    if "email" in session:
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        name = request.form.get("name")
        dob = request.form.get("date")
        email = request.form.get("email")
        password1 = request.form.get("password")
        password2 = request.form.get("confirm_password")
        # if found in database showcase that it's found
        email_found = records.find_one({"email": email})
        if email_found:
            message = 'This email already exists in database'
            return render_template('signup.html', message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('signup.html', message=message)
        else:
            # hash the password and encode it
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            # assing them in a dictionary in key value pairs
            user_input = {'name': name, 'dob': dob, 'email': email, 'membership_status': 0, 'password': hashed}
            # insert it in the record collection
            records.insert_one(user_input)

            # find the new created account and its email
            user_data = records.find_one({"email": email})
            new_email = user_data['email']
            # if registered redirect to logged in as the registered user
            session["email"] = new_email
            return redirect(url_for("dashboard"))
    return render_template('signup.html', message=message)


@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))


@app.route('/iframe/cryptoidx')
def render_cryptoidx():
    if "email" in session:
        return render_template("cryptoidx.html")
    return redirect(url_for("login"))


@app.route('/iframe/altidx')
def render_altidx():
    if "email" in session:
        return render_template("altidx.html")
    return redirect(url_for("login"))


@app.route('/iframe/eurusd')
def render_eurusd():
    if "email" in session:
        return render_template("eurusd.html")
    return redirect(url_for("login"))


@app.route('/cryptoidx')
def cryptoidx():
    if "email" in session:
        email = session["email"]
        user_data = records.find_one({"email": email})
        return render_template("CRYPTO-IDX.html", user_data=user_data)
    return redirect(url_for("login"))


@app.route('/altidx')
def altidx():
    if "email" in session:
        email = session["email"]
        user_data = records.find_one({"email": email})
        return render_template("ALTCOIN.html", user_data=user_data)
    return redirect(url_for("login"))


@app.route('/eurusd')
def euridx():
    if "email" in session:
        email = session["email"]
        user_data = records.find_one({"email": email})
        return render_template("EUR-USD.html", user_data=user_data)


@app.route('/api/getdata/updates/<name>/<date>', methods=['GET', 'POST'])
def get_update_data(name, date):
    url = 'https://n00btrader.com/signal/sig.' + name + '/api/data?type=json&last=1&token=' + session.get(
        'token') + '&date=' + date
    data = requests.get(url)
    data = data.json()
    return data


@app.route('/api/getdata/loaddata/<name>/<date>', methods=['GET', 'POST'])
def load_data(name, date):
    url = 'https://n00btrader.com/signal/sig.' + name + '/api/data?type=json&token=' + session.get(
        'token') + '&date=' + date
    print(url)
    data = requests.get(url)
    data = data.json()
    return data

@app.route('/api/change_membership_status/<email>', methods=['GET', 'POST'])
def change_membership_status(email):
    user_data = records.find_one({'email': email})
    print(user_data)
    records.update_one({'email': email},
    {
    '$set': {
        'membership_status' : 1 - user_data['membership_status']
    }
    })
    return {'data':'data'}


if __name__ == "__main__":
    # app.config['SESSION_TYPE'] = 'filesystem'
    # session.init_app(app)
    app.run()
