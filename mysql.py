import pymysql

def connectDB(cmd):
	db = pymysql.connect("localhost", "root", "password", "mydb", charset='utf8' )
	cursor = db.cursor()
	cursor.execute(cmd)
	data = cursor.fetchone()
	db.commit()
	db.close()
	return data

def inserttodb(userid, liveid):
	cmd = "INSERT INTO xboxliveid(userid,liveid)VALUES(%d,'%s')" % (userid, pymysql.escape_string(liveid))
	connectDB(cmd)

def changeondb(userid, liveid):
	cmd = "UPDATE xboxliveid set liveid='%s' WHERE userid=%d" % (pymysql.escape_string(liveid), userid)
	connectDB(cmd)

def searchindb(userid):
	cmd = "SELECT liveid FROM xboxliveid WHERE userid=%d" % userid
	data = connectDB(cmd)
	try:
		print(data)
		data = ''.join(data)
	except:
		data = -1
	return data

