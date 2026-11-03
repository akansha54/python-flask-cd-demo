
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)

# Secret key for session management
app.secret_key = "my-secret-key"

# Demo login credentials
USERNAME = "admin"
PASSWORD = "Admin@123"



@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username == USERNAME and password == PASSWORD:

            session["username"] = username

            flash("Login Successfully!", "success")

            return redirect(url_for("dashboard"))

        else:
            flash("Invalid username or password!", "error")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    if "username" not in session:
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        username=session["username"]
    )


@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
