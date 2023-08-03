from flask import Flask, render_template
from setup import app


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


if __name__ == '__main__':
    app.run(debug=True)
