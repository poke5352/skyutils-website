from flask import Flask, redirect, request, make_response, render_template, abort
import subprocess
import discord_login
import json
import os
from config import page_config, PAGE_TITLE, MAIN_PAGE, URL, BACKEND_URL, ICON, AUTH, SIGNATURE_KEY, LOGIN_URL, LOGOUT_URL, OWNER
from cryptography.fernet import Fernet

app = Flask(__name__, template_folder=os.getcwd() + "/pages")


def generate_html(current_page, src):
    style = """
            <link rel="icon" href='""" + ICON + """' type="image/x-icon">
            <title>""" + PAGE_TITLE + """</title>
            <style>
            iframe{
                width: 100%;
                border: none;
                position: fixed;
                height: 100%;
                z-index: 0;
                margin: none;
                padding: none;
            }
            html, body {
                margin: 0px;
                padding: 0px;
                border: 0px;
                width: 100%;
                height: 100%;
            }
            </style>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
            <nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #3498DB;">
              <a class="navbar-brand" href='""" + MAIN_PAGE + """' target="_blank">""" + PAGE_TITLE + """</a>
              <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
              </button>
              <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">"""
    for page in page_config:
        if not page_config[page]['restricted'] is True:
            if page_config[page] == current_page:
                style = style + """
                    <li class="nav-item active">
                        <a class="nav-link disabled" href="#">""" + page_config[page]["display_name"] + """<span class="sr-only">(current)</span></a>
                    </li>"""
            else:
                if "link" in page_config[page]:
                    style = style + """
                        <li class="nav-item">
                            <a class="nav-link" href='""" + page_config[page]["link"] + """' target="_blank">""" + page_config[page]["display_name"] + """</a>
                        </li>"""
                else:
                    style = style + """
                        <li class="nav-item">
                            <a class="nav-link" href='""" + URL + page_config[page]["page_link"] + """' target="_self">""" + page_config[page]["display_name"] + """</a>
                        </li>"""
    cookie = request.cookies.get("login_data")
    if cookie is None:
        style = style + """
                    </ul>
                  </div>
                  <button class="btn btn-secondary btn-sm" onclick=" window.location.href = '""" + LOGIN_URL + """'">Discord Login</button>
                </nav>
                <iframe src='""" + src + """' id="streamlit_content" allowfullscreen frameborder="0" wmode="transparent"</iframe>"""
    else:
        fernet_key = Fernet(SIGNATURE_KEY)
        decrypted = json.loads(fernet_key.decrypt(
            cookie.encode("utf-8")).decode())
        style = style + """
                    </ul>
                  </div>
                <div class="nav navbar-right">
                    <img width="28" height="28" style="margin: auto; " src='https://cdn.discordapp.com/avatars/""" + decrypted["id"] + "/" + decrypted["avatar"] + ".png" + """' class="rounded-circle">
                    <ul class="navbar-nav">
                        <li class="nav-item active">
                            <a class="nav-link" href='""" + LOGOUT_URL + """' target="_self">""" + decrypted["username"] + "#" + decrypted["discriminator"] + """</a>
                        </li>
                    </ul>
                </div>
                </nav>
                <iframe src='""" + src + """' id="streamlit_content" allowfullscreen frameborder="0" wmode="transparent"</iframe>"""
    return style


def initial():
    subprocess.Popen(["streamlit", "run", "streamlit_app.py",
                      "--server.port", "8501", "--server.enableCORS", "false"])


initial()


@app.route('/')
def home():
    return generate_html(page_config["creator"], BACKEND_URL + page_config["creator"]["nav_link"])


@app.route('/creator')
def item_creator():
    return generate_html(page_config["creator"], BACKEND_URL + page_config["creator"]["nav_link"])


@app.route('/gallery/<item>')
def gallery(item):
    if item == 'home':
        return generate_html(page_config["gallery"], BACKEND_URL + page_config["gallery"]["nav_link"])
    else:
        return generate_html(page_config["gallery"], BACKEND_URL + page_config["gallery"]["nav_link"] + "&item=" + item)


@app.route('/login')
def login():
    return redirect(AUTH, code=302)


@app.route('/logout')
def logout():
    resp = make_response(render_template(
        "login_success.html", redirect_url=MAIN_PAGE))
    resp.set_cookie('login_data', '', expires=0)
    return resp


@app.route('/login/redirect')
def discord_redirect():
    code = request.args.get("code")
    login = discord_login.exchange_code(code)
    string_data = json.dumps(login)
    fernet_key = Fernet(SIGNATURE_KEY)
    encrypted = fernet_key.encrypt(string_data.encode()).decode("utf-8")
    res = make_response(render_template(
        'login_success.html', redirect_url=MAIN_PAGE))
    res.set_cookie("login_data", value=encrypted)
    return res


@app.route('/admin')
def admin():
    cookie = request.cookies.get("login_data")
    fernet_key = Fernet(SIGNATURE_KEY)
    try:
        decrypted = json.loads(fernet_key.decrypt(
            cookie.encode("utf-8")).decode())
    except:
        return abort(404)
    if decrypted["id"] == OWNER:
        return generate_html(page_config["admin"], BACKEND_URL + page_config["admin"]["nav_link"])
    else:
        return abort(404)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, port=80)
