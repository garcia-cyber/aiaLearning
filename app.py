from flask import Flask , request , session , redirect, render_template , flash
import sqlite3



app = Flask(__name__)
app.secret_key = "mukokoGarciaDev"


##
# Accueil 
@app.route("/")
def home():
    return render_template('front/index.html') 

# login 
#
#
@app.route("/login", methods = ['POST','GET'])
def login():
    if request.method == 'POST':

        user = request.form['username']
        pwd  = request.form['pwd']

        with sqlite3.connect("aia.db") as con :
            cur = con.cursor()
            cur.execute("select * from acteurs where nomUtilisateur = ? and passwordActeur = ? ",[user,pwd]) 
            data  = cur.fetchone()

            if data :
                session['aia'] = True
                session['id']  = data[0]
                session['noms'] = data[1]
                session['email'] = data[2]
                session['user']  = data[3]
                session['role']  = data[4]

                return redirect('/admin')

            else:
                flash("mot de passe incorrecte")  
                  
            

    return render_template('back/auth-login.html')

#
#
# admin
@app.route("/admin")
def admin():
    if 'aia' in session:
        return render_template('back/index.html') 
    else:
        return redirect('/login')
##
#
#  deconnection 
@app.route("/deco")
def deco():
    session.clear()
    return redirect('/')

#
# table-datatable.html
@app.route('/listeUser') 
def listeUser():
    if 'aia' in session:
        with sqlite3.connect('aia.db') as con :
            cur = con.cursor()
            cur.execute("select * from acteurs")
            data = cur.fetchall()

            return render_template('back/table-datatable.html',data = data) 
    else:
        return redirect('/login')
## boucle 

if __name__ == '__main__':
    app.run(debug=True)