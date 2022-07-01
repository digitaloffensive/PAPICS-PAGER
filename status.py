import mysql.connector
import mysql
mydb = mysql.connector.connect(
  host="localhost",
  user="yourinfo",
  password="yourinfo",
  database="yourinfo"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM pics")

myresult = mycursor.fetchall()
for x in myresult:
    f = open("client.txt", "a+")
    f.write(x[0]+';'+x[1]+"\n")
    f.close()
