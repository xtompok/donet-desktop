#!/usr/bin/python3

from flask import Flask
from flask import render_template
from flask import request, Response, redirect
from flask import abort
from functools import partial
import psycopg2 as pg
import json
app = Flask(__name__)

db = "donet"
server = "127.0.0.1"
user = "donet"
password = "vakokokontrihel"

try:
	con = pg.connect(database=db,host=server,user=user,password=password)
except:
	print("Unable to connect to database {} at {}".format(db,server))
	sys.exit(1) 

cur = con.cursor()

def get_attribute(request,name,convert=None,default=None):
	attr = request.args.get(name,None)
	if not attr:
		return (default,"Attribute '{}' undefined".format(name))
	if convert:
		try:
			attr = convert(attr)
		except:
			return (default,"Attribute '{}' in wrong format".format(name))
	return (attr,None)



@app.route("/")
def index():
	return render_template('layout.html')

@app.route("/state/")
def state():
	try:
		cur.execute("SELECT node,name,type,changed,red,green,blue,white FROM state");
	except pg.ProgrammingError as e:
		print("Error in communication with db: {}".format(e.diag.message_primary))
		con.rollback()
		abort(500)
	state = []
	for (node,name,atype,changed,red,green,blue,white) in cur.fetchall():
		if atype == 1:
			color = "#{0:02x}{0:02x}{0:02x}".format(white)
		elif atype == 2:
			color = "#{0:02x}{1:02x}{2:02x}".format(red,green,blue)
		state.append({"node":node,"name":name,"type":atype,"changed":changed, "color": color})
	return json.dumps(state)

@app.route("/set")
def set_color():
	print("Set")
	(name,error) = get_attribute(request,'name',str)
	if not name:
		return error
	(color,error) = get_attribute(request,'color',str)
	if not color:
		return error
	(red,green,blue) = map(partial(int,base=16),[color[0:2],color[2:4],color[4:6]])
	try:
		cur.execute("SELECT type FROM state WHERE name = %s",(name,))
	except pg.ProgrammingError as e:
		print("Error in communication with db: {}".format(e.diag.message_primary))
		con.rollback()
		abort(500)
	mode = cur.fetchall()[0][0]
	print(red,green,blue,mode)
	if (mode == 1):
		try:
			cur.execute("UPDATE state SET white=%s,changed = 1 WHERE name = %s",((red+green+blue)/3,name));
			con.commit();
		except pg.ProgrammingError as e:
			print("Error in communication with db: {}".format(e.diag.message_primary))
			con.rollback()
			abort(500)
		
	if (mode == 2):
		try:
			cur.execute("UPDATE state SET red=%s,green=%s,blue=%s,changed = 1 WHERE name = %s",(red,green,blue,name));
			con.commit();
		except pg.ProgrammingError as e:
			print("Error in communication with db: {}".format(e.diag.message_primary))
			con.rollback()
			abort(500)
	return ('', 204)
	
	
	
