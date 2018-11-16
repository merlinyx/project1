#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
COMS W4111 Introduction to Databases Fall 2018 (Prof. Wu).
Webserver for project 1. 
Team: Victoria Yang (vjy2102), Yuxuan Mei (ym2552).
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response
from film import Film

# Need to create app that is needed for all operations afterwards. 
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
# Have to use this global cache to make this global engine work.
cache = {'engine' : None}

@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request

  The variable g is globally accessible for one request.
  """
  engine = cache['engine']
  try:
    g.conn = engine.connect()
  except:
    print "error creating temporary connection to the db"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass

# Homepage route.
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """
  if app.debug: print request.args
  # List 10 films.
  cursor = g.conn.execute("""SELECT * FROM Film 
    INNER JOIN Filmmaker ON Film.filmmaker_imdblink = Filmmaker.imdblink
    INNER JOIN FilmingLocations ON Film.imdblink = FilmingLocations.film_imdblink
    INNER JOIN NYCLocation ON (FilmingLocations.latitude = NYCLocation.latitude
            AND FilmingLocations.longitude = NYCLocation.longitude) LIMIT 10;""")
  films = []
  for result in cursor: films.append(Film(result)) 
  cursor.close()
  cache['films'] = films
  return render_template("index.html", **cache)

# Film details page route.
@app.route('/film')
def film():
  return render_template("film.html")

@app.route('/filter_by_film', methods=['POST'])
def filter_by_film():
  if app.debug: print request.args
  filmname = '%' + lower(request.form['film']) + '%'
  if app.debug: print filmname
  qry = """SELECT * FROM Film 
    INNER JOIN Filmmaker ON Film.filmmaker_imdblink = Filmmaker.imdblink
    INNER JOIN FilmingLocations ON Film.imdblink = FilmingLocations.film_imdblink
    INNER JOIN NYCLocation ON (FilmingLocations.latitude = NYCLocation.latitude
            AND FilmingLocations.longitude = NYCLocation.longitude)
    WHERE LOWER(Film.title) LIKE :film_searchstring LIMIT 10;"""
  cursor = g.conn.execute(text(qry), film_searchstring = filmname)
  films = []
  for result in cursor: films.append(Film(result)) 
  cursor.close()
  cache['films'] = films
  return render_template("index.html", **cache)

@app.route('/filter_by_location', methods=['POST'])
def filter_by_location():
  if app.debug: print request.args
  location = '%' + lower(request.form['location']) + '%'
  if app.debug: print location
  qry = """SELECT * FROM Film 
    INNER JOIN Filmmaker ON Film.filmmaker_imdblink = Filmmaker.imdblink
    INNER JOIN FilmingLocations ON Film.imdblink = FilmingLocations.film_imdblink
    INNER JOIN NYCLocation ON (FilmingLocations.latitude = NYCLocation.latitude
            AND FilmingLocations.longitude = NYCLocation.longitude)
    WHERE LOWER(NYCLocation.address) LIKE :location_searchstring LIMIT 10;"""
  cursor = g.conn.execute(text(qry), location_searchstring = location)
  films = []
  for result in cursor: films.append(Film(result)) 
  cursor.close()
  cache['films'] = films
  return render_template("index.html", **cache)

if __name__ == "__main__":
  import argparse
  DB_SERVER = "w4111.cisxo09blonu.us-east-1.rds.amazonaws.com"
  parser = argparse.ArgumentParser()
  parser.add_argument('--host', default='0.0.0.0', help='host ip address')
  parser.add_argument('--port', default=8111, help='port number', type=int)
  parser.add_argument('--user', default='ym2552', help='username for connecting to the db')
  parser.add_argument('--pwd', required=True, help='password for connecting to the db')
  parser.add_argument('--debug', action='store_true', help='whether to run in debug mode')
  parser.add_argument('--threaded', action='store_true', help='whether to run in multi threads')
  args = parser.parse_args()
  
  # The Database URI should be in the format of: 
  #     postgresql://USER:PASSWORD@<IP_OF_POSTGRE_SQL_SERVER>/<DB_NAME>
  user = args.user
  pwd = args.pwd
  DB_URI = 'postgresql://%s:%s@%s/w4111' % (user, pwd, DB_SERVER)
  # Create a database engine that connects to the database of the given URI. 
  engine = create_engine(DB_URI)
  cache['engine'] = engine
  if args.debug: print 'engine created'

  # Below is the first batch of queries to prepare the dropdown items.
  try:
    tconn = engine.connect()
  except:
    print "error creating temporary connection to the db"
    import traceback; traceback.print_exc()
    tconn = None
  
  cursor = tconn.execute("""SELECT DISTINCT borough from NYCLocation;""")
  boroughs = []
  for result in cursor: boroughs.append(result[0])
  cursor.close()
  cache['boroughs'] = boroughs

  cursor = tconn.execute("""SELECT DISTINCT neighborhood from NYCLocation;""")
  neighborhoods = []
  for result in cursor: neighborhoods.append(result[0])
  cursor.close()
  cache['neighborhoods'] = neighborhoods

  try:
    tconn.close()
  except Exception as e:
    pass

  # Now ready to serve the page.
  HOST, PORT = args.host, args.port
  print 'running on %s:%d' % (HOST, PORT)
  app.run(host=HOST, port=PORT, debug=args.debug, threaded=args.threaded)
