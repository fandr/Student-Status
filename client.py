#Student information system client
from optparse import OptionParser
import socket

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#Define command line options
parser = OptionParser()
parser.add_option("-a","--add",dest="addStudentName",
		help="Add a new student STUDENT")
parser.add_option("-l", "--list", action="store_true", dest="list",
                help="List all students")
(options,args) = parser.parse_args()

print "[*] Connecting..."
sock.connect(('localhost',8080))
print "[+] Connected succesfully!"

if options.list:
	sock.send("list\n")
	data = sock.recv(4048)
	data = data.replace(",","")
	data = data.replace("(","")
	dataL = data.split(")")
	print "** Student Status **"
	for item in dataL:
		print item
	exit()

if options.addStudentName:
	sock.send('add %s' %options.addStudentName)
	print "'%s' created" %options.addStudentName
exit()
