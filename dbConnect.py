import mysql.connector
from mysql.connector import Error

def search(errorType,errorStatement):
    try: 
         connection = mysql.connector.connect(host="",port=3306,database="ErrorResolver",user= "",password= "")
         cursor = connection.cursor()
         sql_fetch_query ="""select answer from Eror where error_type=%s and error_statement=%s;"""
         name=(errorType,errorStatement)
         cursor.execute(sql_fetch_query,name)
         record = cursor.fetchall()
         return record

    except mysql.connector.Error as error:
         print("Failed to search data from MySQL table {}".format(error))
         return -1
    
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
            
def insert(errorType,errorStatement,answer):
    try: 
         connection = mysql.connector.connect(host="",port=3306,database="ErrorResolver",user= "",password= "")
         cursor = connection.cursor()
         l=count()[0]
         if(l[0]>2):
             delete(int(l[1]))
         sql_fetch_query ="""insert into Eror values ('',%s,%s,%s)"""
         name=(errorType,errorStatement,answer,)
         cursor.execute(sql_fetch_query,name)
         connection.commit()
         return True

    except mysql.connector.Error as error:
         print("Failed to insert from MySQL table {}".format(error))
         return False
    
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def count():
    try: 
         connection = mysql.connector.connect(host="",port=3306,database="ErrorResolver",user= "",password= "")
         cursor = connection.cursor()
         sql_fetch_query ="""select Count(*),min(id) from Eror;"""
         name=()
         cursor.execute(sql_fetch_query,name)
         record = cursor.fetchall()
         return record

    except mysql.connector.Error as error:
         print("Failed to count from MySQL table {}".format(error))
         return -1
    
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
            
def delete(id):
    try: 
         connection = mysql.connector.connect(host="",port=3306,database="ErrorResolver",user= "",password= "")
         cursor = connection.cursor()
         sql_fetch_query ="""delete from Eror where id=%s"""
         name=(id,)
         cursor.execute(sql_fetch_query,name)
         connection.commit()
         return 1

    except mysql.connector.Error as error:
         print("Failed to delete data from MySQL table {}".format(error))
         return -1
    
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    
    
