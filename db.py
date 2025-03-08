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



con.commit()