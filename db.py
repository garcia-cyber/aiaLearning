import sqlite3 


con = sqlite3.connect("aia.db") 



##
## 
con.execute("""

    create table if not exists acteurs(
            idActeur integer primary key autoincrement,
            nomsActeur varchar(30),
            emailActeur varchar(40) , 
            nomUtilisateur varchar(30) , 
            fonctionActeur varchar(15) default 'apprenant' ,
            passwordActeur varchar(30)
             )
""") 

#info defaut 
#con.execute("insert into acteurs(nomsActeur,emailActeur,nomUtilisateur,fonctionActeur,passwordActeur) values('admin','admin@gmail.com','admin','admin','admin')")

## creation de la table module 
con.execute("""
            create table if not exists modules
            (
            idModule integer primary key autoincrement ,
             libModule varchar(20)
            )
            """)

##
# creation de la table formation 
con.execute("""
            create table if not exists formations(
            idFormation integer primary key autoincrement,
            moduleID integer , 
            acteurID integer , 
            statut char(3) default 'non' ,
            foreign key(moduleID) references modules(idModule),
            foreign key(acteurID) references acteurs(idActeur) )

            """)
con.commit()