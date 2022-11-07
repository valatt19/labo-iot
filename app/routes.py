from app import app
from flask import render_template, redirect
from flask import url_for, request

##########
# ROUTES #
##########

@app.route("/")
def hello_world():
    return render_template("index.html")


#######
# RUN #
#######
if __name__ == "__main__":
        app.run()