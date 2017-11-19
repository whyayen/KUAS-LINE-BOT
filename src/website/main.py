from flask import (Flask, render_template, request,
                   redirect, make_response, url_for)

from modules.bus.bus_tool import ikuaslogin
import json
import os
import yaml
import re
import requests
import random
import string

app = Flask(__name__)

with open(os.path.dirname(__file__) + "/config.yml", 'r') as f:
    CONFIG = yaml.load(f)


URL = "http://line.yanjun.tw"
LINELOGIN = "https://access.line.me/oauth2/v2.1/authorize?response_type=code\
        &client_id=%s&redirect_uri=%s&state=%s&scope=profile"


@app.route("/linelogin", methods=['GET'])
def lineLogin():
    # line login valid

    session = requests.session()

    payload = {"client_id": CONFIG['client_id'],
               "grant_type": "authorization_code",
               "code": request.args.get('code'),
               "redirect_uri": URL + '/linelogin',
               "client_secret": CONFIG['client_secret']
               }

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    r = session.post("https://api.line.me/oauth2/v2.1/token",
                     headers=headers,
                     data=payload
                     )

    data = json.loads(r.text)
    try:
        r = session.get(
                "https://api.line.me/v2/profile",
                headers={"Authorization": "Bearer %s" % data['access_token']}
                )
        datap = json.loads(r.text)
        response = make_response(redirect('/'))
        response.set_cookie('userID', datap['userId'], 2592000*6)
        return response
    except:
        randomStr = ''
        for x in range(10):
            randomStr.join(random.choice(string.ascii_letters + string.digits))

        return redirect(LINELOGIN % (CONFIG['client_id'],
                                     URL + "/linelogin",
                                     randomStr))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if(request.cookies.get('userID') is None):
        return redirect('/')
    elif(request.cookies.get('stdID') is not None and
         request.cookies.get('apiKey') is not None):
        return redirect('/')

    if(request.method == 'POST'):

        if(not request.form.get('accept') or
           request.form.get('accept') is None):

            return render_template("login.html", errormsg="請同意服務條款")

        else:
            login = ikuaslogin(request.form.get('username'),
                               request.form.get('password'))

            if(login.get_userKey() == ""):
                return render_template("login.html", errormsg="帳號或密碼錯誤")
            else:
                response = make_response(redirect(url_for('index')))
                response.set_cookie('stdID',
                                    request.form.get('username'),
                                    2592000*6)
                response.set_cookie('apiKey', login.get_userKey(), 2592000*6)
                return response
    else:
        return render_template("login.html", errormsg="")


@app.route("/")
def index():

    if(request.cookies.get('userID') is None):
        randomStr = ''
        for x in range(10):
            randomStr.join(random.choice(string.ascii_letters +
                           string.digits))

        return redirect(LINELOGIN % (CONFIG['client_id'],
                                     URL + "/linelogin",
                                     randomStr))

    elif(request.cookies.get('stdID') is None or
         request.cookies.get('apiKey') is None):

        return redirect(URL + "/login")

    return render_template("index.html")


if __name__ == "__main__":
    app.run()
