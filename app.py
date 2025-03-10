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
    

###
# ###
# creation de compte
# 
# 
@app.route("/apprenant", methods = ['POST','GET'])
def apprenant():
    if request.method == 'POST':
        noms = request.form['noms'] 
        email = request.form['email']
        user = request.form['user']
        pwd  = request.form['pwd']
        pwd2 = request.form['pwd2']
        role = 'apprenant'

        with sqlite3.connect("aia.db") as con :
            # verification du email 
            mail = con.cursor()
            mail.execute("select * from acteurs where emailActeur = ? ",[email]) 
            dataMail = mail.fetchone()

            # verification du nom utilisateur 
            use = con.cursor()
            use.execute("select * from acteurs where nomUtilisateur = ?", [user]) 
            dataUse = use.fetchone() 

            if dataMail:
                flash('le email existe deja ')
            elif dataUse:
                flash("le nom d'utilisateur existe deja") 
            elif pwd2 == pwd:
                add = con.cursor()
                add.execute("insert into acteurs(nomsActeur,emailActeur,nomUtilisateur,fonctionActeur,passwordActeur) values(?,?,?,?,?)",[noms,email,user,role,pwd])
                con.commit()
                
                return redirect('/login')
            else:
                flash("le mot de passe doit etre conforme")        


        

    return render_template('back/auth-register.html')


###
# ###
# creation de compte formateur
# 
# 
@app.route("/formateur", methods = ['POST','GET'])
def formateur():
    if request.method == 'POST':
        noms = request.form['noms'] 
        email = request.form['email']
        user = request.form['user']
        pwd  = request.form['pwd']
        pwd2 = request.form['pwd2']
        role = 'formateur'

        with sqlite3.connect("aia.db") as con :
            # verification du email 
            mail = con.cursor()
            mail.execute("select * from acteurs where emailActeur = ? ",[email]) 
            dataMail = mail.fetchone()

            # verification du nom utilisateur 
            use = con.cursor()
            use.execute("select * from acteurs where nomUtilisateur = ?", [user]) 
            dataUse = use.fetchone() 

            if dataMail:
                flash('le email existe deja ')
            elif dataUse:
                flash("le nom d'utilisateur existe deja") 
            elif pwd2 == pwd:
                add = con.cursor()
                add.execute("insert into acteurs(nomsActeur,emailActeur,nomUtilisateur,fonctionActeur,passwordActeur) values(?,?,?,?,?)",[noms,email,user,role,pwd])
                con.commit()
                
                return redirect('/login')
            else:
                flash("le mot de passe doit etre conforme")        


        

    return render_template('back/formateur.html') 

# ajout de module
#
# form-layout.html
@app.route("/addModule" ,methods =['POST','GET'] )
def addModule():
    if 'aia' in session:
        if request.method == 'POST':
            module = request.form['module']

            with sqlite3.connect("aia.db") as con :
                md = con.cursor()
                md.execute("select * from modules where libModule = ?",[module])
                dataMd = md.fetchone()

                if dataMd:
                    flash("le module existe deja dans le systeme !!!".upper())
                else:
                    cur = con.cursor()
                    cur.execute("insert into modules(libModule) values(?)",[module])
                    con.commit()
                    flash(f" {module} ajoutee avec succes !!!!!")
        return render_template('back/form-layout.html') 
    else:
        return redirect('/login')

##
#
# Liste de module 
#
#
@app.route('/listeModule') 
def listeModule():
    if 'aia' in session:
        with sqlite3.connect('aia.db') as con :
            cur = con.cursor()
            cur.execute("select * from modules")
            data = cur.fetchall()

            return render_template('back/listeModule.html',data = data) 
    else:
        return redirect('/login')

###
##
# messages
# application-email.html
@app.route('/message')
def message():
    if 'aia' in session:
        return render_template('back/application-email.html')
    else:
        return redirect('/') 
    
#
#
#formation 
@app.route('/formation', methods=['POST','GET'])
def formation():
    if 'aia' in session:
        if request.method == 'POST':
            formation = request.form['formation']
            

            with sqlite3.connect("aia.db") as con :
                #verification de la formation 
                ver = con.cursor()
                ver.execute("select * from formations where moduleID = ? and acteurID = ?",[formation,session['id']])
                dataV = ver.fetchone()

                if dataV:
                    flash("vous suivez deja ce module !!!!")
                elif int(formation) == 1 :
                    
                    cur = con.cursor()
                    cur.execute("insert into formations(moduleID,acteurID) values(?,?)",[formation,session['id']]) 
                    con.commit()
                    cur.close()

                    flash("veillez consulte votre messagerie pour la suite de la formation")


                    
                else:
                    cur = con.cursor()
                    cur.execute("insert into formations(moduleID,acteurID) values(?,?)",[formation,session['id']]) 
                    con.commit()
                    cur.close()

                    flash("veillez consulte votre messagerie pour la suite de la formation")
                    

        
        with sqlite3.connect('aia.db') as con:

            cur = con.cursor()
            cur.execute("select * from modules") 
            data = cur.fetchall()

            return render_template('back/formation.html',data = data)  
    else:
        return redirect('/login')

#
# #
# chat
# 
@app.route('/chat')
def chat():
    if 'aia' in session:
        return render_template('back/application-chat.html') 
    else: 
        return redirect('/')    
    
#
# liste des informations 
# 
@app.route('/listeFormation')
def listeFormation():
    if 'aia' in session:
        with sqlite3.connect("aia.db") as con :
            cur = con.cursor()
            cur.execute("select idFormation,nomsActeur,nomUtilisateur,emailActeur,libModule,statut from formations inner join acteurs on formations.acteurID = acteurs.idActeur inner join modules on formations.moduleID = modules.idModule")
            data = cur.fetchall()

        return render_template("back/listeFormation.html", data = data)  
    else:
        return redirect('/')    
    
##
#
# suppresion depuis la table formation
@app.route("/dropFormation/<string:idFormation>", methods = ['POST','GET'])
def dropFormation(idFormation):
    with sqlite3.connect('aia.db') as con :
        cur = con.cursor()
        cur.execute("delete from formations where idFormation = ?",[idFormation]) 
        con.commit()
    
        return redirect('/listeFormation')  

##
# #
# 
# autorisation    

## boucle 


if __name__ == '__main__':
    app.run(debug=True)