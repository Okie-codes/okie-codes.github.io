
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
import numpy as np
from matplotlib.figure import Figure
from io import BytesIO
import base64

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    return render_template ("index.html")

@app.route("/graphs.html", methods=["GET", "POST"])
def graphs():
    return render_template("graphs.html")

@app.route("/nongraph.html", methods=["GET", "POST"])
def nongraphs():
    if request.method=="POST":
        m = request.form.get("m")
        A = request.form.get("A")
        w = request.form.get("w")
        phi = request.form.get("phi")
        b = request.form.get("b")

        if (not m) or (not A) or (not w) or (not phi) or (not b):
            return render_template("index.html")

        fig = Figure()
        ax1, ax2 = fig.subplots(2)

        t = np.linspace(0,100,1000)

        y0 = float(A)  * np.cos (float(w) * t + float(phi))
        ax1.plot(t, y0)
        ax1.set_title("Undamped")

        y = (np.exp(-float(b)/(2*float(m)) * t)) * y0
        ax2.plot(t,y)
        ax2.set_title("Damped")

        buf = BytesIO()
        fig.savefig(buf, format="png")
        
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        return f"<img src='data:image/png;base64,{data}'/>"
    else:
        return render_template("nongraph.html")

@app.route("/about.html", methods=["GET", "POST"])
def about():
    return render_template("about.html")

@app.route("/resources.html", methods=["GET", "POST"])
def resources():
    return render_template("resources.html")

if __name__ == "__main__":
    app.run(debug=True)

