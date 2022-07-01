import mysql.connector
import mysql
import sys
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="yourinfo",
  database="yourinfo"
)
udel = sys.argv[1]
#print(udel)



mycursor = mydb.cursor()

sql = "DELETE FROM pics  WHERE Email = "+udel
#print(sql)

mycursor.execute(sql)

mydb.commit()

#print(mycursor.rowcount, "record(s) deleted")
