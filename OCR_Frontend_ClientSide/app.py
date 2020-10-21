from flask import Flask, render_template, request, url_for, redirect, make_response, flash
import secrets
from config import SECRET_KEY, JWT_SECRET_KEY
from flask_jwt_extended import JWTManager
from api_methods import (login_api, register_api, document_api, documents_api,
                        logout_api, searchkeywords_api, reader_api,
                        validateUser_api)
from io import BufferedReader
from side_methods import allowed_file, scan_OCR

app = Flask(__name__)
jwt_manger = JWTManager(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
app.config["SECRET_KEY"] = SECRET_KEY

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if len(password) < 5:
            flash("Password length needs to be greater than 5")
            return redirect(url_for("login"))
        result = login_api(username, password)
        status = result["status"]
        message = result["message"]
        if status == 1:
            flash(message)
            return redirect(url_for("login"))
        token = result["access_token"]
        response = make_response(redirect(url_for("main")))
        response.set_cookie('token', token)
        flash(message)
        return response

    token = request.cookies.get("token")

    if token:
        result = validateUser_api(token)
        status = result["status"]
        message = result["message"]
        if status == 0:
            return redirect(url_for("main"))
    return render_template("login_register/login.html", title="Login Page")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        username = request.form["username"]
        password = request.form["password"]
        if len(password) < 5:
            flash("Password length needs to be greater than 5")
            return redirect(url_for("login"))
        result = register_api(first_name, last_name, username, password)
        status = result["status"]
        message = result["message"]
        if status == 1:
            flash(message)
            return redirect(url_for("register"))
        flash(message)
        return redirect(url_for("login"))

    token = request.cookies.get("token")
    if token:
        result = validateUser_api(token)
        status = result["status"]
        message = result["message"]
        if status == 0:
            return redirect(url_for("main"))
    return render_template("login_register/register.html", title="Register Page")

@app.route("/")
def main():
    token = request.cookies.get("token")
    if token:
        result = validateUser_api(token)
        status = result["status"]
        message = result["message"]
        if status == 1:
            flash(message)
            return redirect(url_for("login"))
        user = result["user"]
    else:
        return redirect(url_for("login"))
    return render_template("main.html", user=user, tile="Main Page")

@app.route("/logout")
def logout():
    token = request.cookies.get("token")
    result = logout_api(token)
    status = result["status"]
    message = result["message"]
    flash(message)
    if status == 1:
        return redirect(url_for("main"))
    return redirect(url_for("login"))

@app.route("/documents")
def show_documents():
    token = request.cookies.get("token")
    if token:
        result = validateUser_api(token)
        status = result["status"]
        message = result["message"]
        if status == 1:
            flash(message)
            return redirect(url_for("login"))
        docs = documents_api(token)["documents"]
    else:
        return redirect(url_for("login"))
    return render_template("documents/documents.html", docs=docs, title="Documents")

@app.route("/document/<string:doc_name>")
def show_document(doc_name):
    token = request.cookies.get("token")
    if token:
        result = validateUser_api(token)
        status = result["status"]
        message = result["message"]
        if status == 1:
            flash(message)
            return redirect(url_for("login"))
        result = document_api(doc_name, token, "GET")
        status = result["status"]
        if status == 1:
            doc = None
        else:
            doc = result["documents"]
    else:
        return redirect(url_for("login"))
    return render_template("documents/document.html", doc=doc, title="Document")

@app.route("/delete/document/<string:doc_name>")
def delete_document(doc_name):
    token = request.cookies.get("token")
    if token:
        result = validateUser_api(token)
        status = result["status"]
        message = result["message"]
        if status == 1:
            flash(message)
            return redirect(url_for("login"))
        result_callback = document_api(doc_name, token, "DELETE")
        status = result_callback["status"]
        message = result_callback["message"]
        flash(message)
        return redirect(url_for("show_documents"))

    else:
        return redirect(url_for("login"))

@app.route("/update/document/<string:doc_name>", methods=["GET", "POST"])
def update_document(doc_name):
    token = request.cookies.get("token")
    if not token:
        return redirect(url_for("login"))
    result = validateUser_api(token)
    status = result["status"]
    if status == 1:
        message = result["message"]
        flash(message)
        return redirect(url_for("login"))
    if request.method == "POST":
        new_name = request.form["new_name"]
        content = request.form["update_content"]
        result = document_api(doc_name, token, "PUT", content, new_name)
        message = result["message"]
        flash(message)
        return redirect(url_for('show_documents'))

    result = document_api(doc_name, token, "GET")
    doc = result["documents"]
    return render_template("documents/update_document.html", doc=doc)

@app.route("/upload/document", methods=["GET", "POST"])
def upload_document():
    token = request.cookies.get("token")
    if not token:
        return redirect(url_for("login"))
    result = validateUser_api(token)
    status = result["status"]
    if status == 1:
        message = result["message"]
        flash(message)
        return redirect(url_for("login"))
    if request.method == "POST":
        new_name = request.form["new_name"]
        content = request.form["update_content"]
        result = document_api(new_name, token, "POST", content)
        message = result["message"]
        flash(message)
        return redirect(url_for('show_documents'))
    return render_template("documents/upload_document.html")

@app.route("/readImage", methods=["GET", "POST"])
def read_image():
    doc = "None"
    token = request.cookies.get("token")
    if not token:
        return redirect(url_for("login"))
    result = validateUser_api(token)
    status = result["status"]
    if status == 1:
        message = result["message"]
        flash(message)
        return redirect(url_for("login"))
    if request.method == "POST":
        file = request.files["file"]
        if file is not None:
            if file.filename == '':
                return {"status": 1, "message": "No file found. Please input file"}, 400
        else:
            return {"status": 1, "message": "No file found. Please input file"}, 400

        if not allowed_file(file.filename):
            return {"status": 1, "message": "File type not support. Please input the following type: PNG, JPG, JPEG"}, SC_BAD_REQUEST

        image_file = BufferedReader(file)
        doc_content = scan_OCR(image_file)
        message = "Successfully"
        flash(message)
    return render_template("read_image.html", doc=doc)

@app.route("/searchKeywords", methods=["GET", "POST"])
def search_keywords():
    docs = "None"
    token = request.cookies.get("token")
    if not token:
        return redirect(url_for("login"))
    result = validateUser_api(token)
    status = result["status"]
    if status == 1:
        message = result["message"]
        flash(message)
        return redirect(url_for("login"))

    message = "Content Display Here!"
    if request.method == "POST":
        searchKeywords = request.form["keywords"]
        result = searchkeywords_api(token, searchKeywords)
        status = result["status"]
        message = result["message"]
        if status == 0:
            docs = result["documents"]
            if len(docs) == 0:
                docs = "None"
        flash(message)
    return render_template("search_keywords.html", docs=docs, message=message)
