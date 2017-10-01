#!/usr/bin/python3

import sys
import psycopg2
import serial
import time

db = "donet"
server = "127.0.0.1"
user = "donet"
password = "vakokokontrihel"

retries = 10

CMD_PING = 0x01
CMD_PWM_ONE = 0x02
CMD_PWM_THREE = 0x03


try:
	con = psycopg2.connect(database=db,host=server,user=user,password=password)
except:
	print("Unable to connect to database {} at {}".format(db,server))
	sys.exit(1) 

cur = con.cursor()

if len(sys.argv) == 1:
	port = "/dev/ttyUSB0"
else:
	port = sys.argv[1]

try:
	ser = serial.open(port,115200,timeout=1000)
except 


def check_db():
	cur.execute("SELECT node,type,red,green,blue,white FROM state WHERE changed = 1")
	for (node,atype,red,green,blue,white) in cur.fetchall():
		if (atype == 1):
			result = set_w_color(node,white)
			process_result(result)
		if (atype == 2):
			result = set_rgb_color(node,red,green,blue)
			process_result(result)

def commit_to_db(node):
	cur.execute("UPDATE state SET changed = 0 WHERE node = %s",(node,))
	con.commit()

def log_to_db(module,node,state,cmt):
	cur.execute("INSERT INTO events (module,node,state,cmt) VALUES (%s,%s,%s,%s)",(module,node,state,cmt))


def process_result(line):
	if ";" not in line:
		print("Returned: {}".format(line))
		return False
	try:
		(module,node,state,cmt) = line.split(";",3)
	except ValueError:
		print("Failed to split line {}".format(line))
		return False
	if (state=="OK"):
		commit_to_db(node)

	log_to_db(module,node,state,cmt)	
	return True
		
def scan_devices():
	pass
	 	
def set_w_color(node,value):
	print("Setting white to {} at node {}".format(value,node))
	line = send_packet(node,CMD_PWM_ONE,(value,))
	return process_result(line)

def set_rgb_color(node,red,green,blue):
	print("Setting RGB to ({},{},{}) at node {}".format(red,green,blue,node))
	line = send_packet(node,CMD_PWM_THREE,(red,green,blue))
	return process_result(line)

def send_packet(node,cmd,data):
	bdata = bytearray()
	bdata.append(node)
	bdata.append(cmd)
	for d in data:
		bdata.append(d)
	ser.write(bdata)
	line = ser.readline()
	if line[:-1] != '\n':
		print("Timeout occured while reading line")
		return line
	return line[:-1]


while (True):
	check_db()
	time.sleep(1)
