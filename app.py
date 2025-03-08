from flask import Flask , request , session , redirect, render_template
import sqlite3



app = Flask(__name__)
app.secret_key = "mukokoGarciaDev"


##
# Accueil 
@app.route("/")
def home():
    return render_template('front/index.html') 



## boucle 

if __name__ == '__main__':
    app.run(debug=True)