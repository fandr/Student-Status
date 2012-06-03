##
#Description: This script will manage incoming commands
##

import socket,MySQLdb
from optparse import OptionParser

#Script information variables
script_version = '1.0'

#Listening server parameters
webhost = ''
webport = 8080

#The dbHandler class will handle everything mysql-related
class dbHandler(object):
	dbconnected = False
	#Constructor
	def __init__(self):
		#The database connection parameters
		self.__dbhost = 'connect-utb.com'
		self.__dbuser = 'connect_fihuser'
		self.__dbname = 'connect_fih'
		self.__dbpass = 'Pass321!'
		self.__db = ""
	#Connect to the db
	def connectToDb(self):
		print "Connecting to the database at %s" %self.dbhost
		#attempt to connect to db
		try:
			self.db = MySQLdb.connect(self.dbhost, self.dbuser,self.dbpass,self.dbname)
			print "Connected!"
		except Exception as ex:
			print "Error connecting to database"
			print ex
			print "Shutting down..." 
			exit()

	#Add a student to the student table
	def addStudent(self, studentName):
		print "adding %s to database.." %studentName
		#Define a new db cursor
		cursor = self.db.cursor()
		#execute SQL query
		cursor.execute("INSERT INTO studentInfo (studentName,studentStatus) VALUES('%s','Active')" %studentName)
		print "[+]'%s' added successfully" %studentName	
	#Remove a student
	def removeStudent(self, studentName):
		print "This feature is not implemented yet. Students need to work harder!!"
	def updateStudentStatus(self, studentName):
		print "Students must implement this as well"
	def addStudentComment(self, studentName):
		print "Students must make it possible to add comments to a student"
	def listAll(self):
		#define new db cursor
		cursor = self.db.cursor()
		#execute SQL
		cursor.execute("SELECT * FROM studentInfo")
		#define the list we will use for the returned data
		retData = []
		#fetch all rows
		while(1):
			row = cursor.fetchone()
			if row == None:
				break
			retData += str(row)
		return retData

#Handle commandline options..
parser = OptionParser()
parser.add_option("-v", "--verbose", action="store_true", dest="verb",
		help="Print out incoming data")
(options, args) = parser.parse_args()
#Start script
print "FIH Student information system server %s starting up" %script_version
#Initate DB connection with parameters
db = dbHandler()
db.dbhost = 'connect-utb.com'
db.dbuser = 'connect_fihuser'
db.dbname = 'connect_fih'
db.dbpass = 'Pass321!'
db.connectToDb()
#Initate Web server
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
sock.bind((webhost,webport))
sock.listen(1)
#Web server initiated, waiting for requests
while 1:
	csock, caddr = sock.accept()
	print "[*] New connection from: %s" %str(caddr)
	cfile = csock.makefile('rw',0)
	#Protocol exchange
	while 1:
		line = cfile.readline().strip()
		if options.verb:
			print "[*]Command received: %s" %line
		if line.startswith('rm '):
			#split string to detect name
			sName = line.split(" ")
			db.removeStudent('%s' % sName[1:2])
			cfile.write("Return values come here")
		elif line.startswith('add '):
			#split string to detect name
			sName = line.split(" ")
			db.addStudent('%s' %sName[1])
		elif line.startswith('list'):
			#Collect the returned data and send it to the socket client
			allStudents = (db.listAll())
			csock.send(",".join(allStudents))

		cfile.close
		csock.close()
		break

