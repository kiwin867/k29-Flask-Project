# import necessary libraries from Flask,
# psycopg2 for PSQL, and base64 for encoding
from flask import Flask, request, render_template, make_response
import psycopg2
import base64
# create a new Flask web-app instance
myapp = Flask(__name__)
logged_in_user = "Guest" # default user if not logged in
# setup the needed database connection details.
# they may of course change depending on your setting.
DB_HOST = "localhost" # database on local host
DB_PORT = "5432" # port used to talk to psql
DB_NAME = "flaskdb" # database name
DB_USER = "k29" # username is k29
DB_PASS = "1234" # k29 password
# establish the connection to postesql using the preset creds
conn = psycopg2.connect(
host=DB_HOST,
port=DB_PORT,
dbname=DB_NAME,
user=DB_USER,
password=DB_PASS
)
# a route defines a map on how the app responds to a client request
# often fired from a browser or mobile app for a specific
# URL and an HTTP method such as GET, POST, DELETE
#

# route registration page which accepts both GET and POST HTTP requests
@myapp.route('/addfriend', methods=['GET', 'POST'])
def addfriend():
    if request.method == 'POST':
     # retrieve the data sent through the POST request
     email = request.form['email']
     # create a cursor object using the database connection
     cursor = conn.cursor()
     cursor.execute('SELECT fname, lname, email FROM flusers WHERE email = %s', (email,))
     existing_friend = cursor.fetchone()
     first_name = existing_friend[0]
     last_name = existing_friend[1]
     cursor.execute('SELECT id FROM flusers WHERE email = %s', (logged_in_user,))
     userid = cursor.fetchone()
     if existing_friend and logged_in_user != "Guest":
     # execute an INSERT command to add the new friend to the 'flfriends' table
      insert_command = """
      INSERT INTO flfriends (fid, fname, lname, email)
      VALUES (%s, %s, %s, %s)
      """;
      insert_data = (userid, first_name, last_name, email);
      cursor.execute(insert_command, insert_data);
     # commit the transaction to save the changes in the database
      conn.commit()
     else:
       return "Friend not found or you are not logged in. Please try again."
     # close the cursor to free up resources
     cursor.close()
     return render_template('home.html', user=logged_in_user)
    return render_template('addfriend.html')
@myapp.route('/viewfriends')
def viewfriends():
    # if logged_in_user == "Guest":
    #     return "Please log in to view your friends."
    cursor = conn.cursor()
    print(logged_in_user)
    cursor.execute('SELECT id FROM flusers WHERE email = %s', (logged_in_user,))
    userid = cursor.fetchone()
    cursor.execute('SELECT fname, lname, email FROM flfriends WHERE fid = %s', (userid,))
    friends_data = cursor.fetchall()
    friends_list = []
    for friend in friends_data:
        first_name, last_name, email = friend
        friends_list.append({
        'first_name': first_name,
        'last_name': last_name,
        'email': email
        })
    cursor.close()
    return render_template('viewfriends.html', friends=friends_list)
@myapp.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    email = request.form['email']
    password = request.form['password']
    cursor = conn.cursor()
    cursor.execute('SELECT email FROM flusers WHERE email = %s AND pass = %s', (email, password))
    user = cursor.fetchone()
    cursor.close()
    if user:
      global logged_in_user
      logged_in_user = email
      print(logged_in_user)
      return render_template('home.html', user=logged_in_user)
    else:
      return "Invalid email or password. Please try again."
  return render_template('login.html')
@myapp.route('/')
def home():
# this route designates all gets started:
# render and return the home page
# found within templates dir
 print(logged_in_user)
 return render_template('home.html', user=logged_in_user)

@myapp.route('/register', methods=['GET', 'POST'])
def register():
# check if the request method is POST
# POST means that a form data has been submitted
 if request.method == 'POST':
# retrieve the data off the HTML-form sent through
# the POST request
  first_name = request.form['first_name']
  last_name = request.form['last_name']
  email = request.form['email']
  password = request.form['password'] # this should be hashed..
  photo = request.files['photo'].read()
# read in the binary content of the uploaded photo
  dob = request.form['dob'] #optional
#
# create a cursor object using the database connection
# this is how prepared SQL statements can be executed.
  cursor = conn.cursor() # this also implies a BEGIN;
  cursor.execute('SELECT email FROM flusers WHERE email = %s', (email,))
  existing_user = cursor.fetchone()
  if existing_user:
    cursor.close()
    return "Email already registered. Please use a different email."
  if dob == '':
    intercomm = """
    INSERT INTO flusers (fname, lname, email, pass, photo)
    VALUES (%s, %s, %s, %s, %s)
    """;
    interdata = (first_name, last_name, email, password, psycopg2.Binary(photo),);
    cursor.execute(intercomm, interdata);
  else:
# exec an INSERT to enter the form data into the 'flusers' table
    insertcomm = """
    INSERT INTO flusers (fname, lname, email, pass, photo, dob)
    VALUES (%s, %s, %s, %s, %s, %s)
    """;
    insertdata = (first_name, last_name, email, password, psycopg2.Binary(photo), dob,);
    cursor.execute(insertcomm, insertdata);
# commit the transaction to save the changes in the database
  conn.commit()
# from the database, get the photo that was just uploaded
# using the email as key
  cursor.execute(
'SELECT photo FROM flusers WHERE email = %s', (email,)
)
  photo_data = cursor.fetchone()[0]
# get the first and only column from the first row of results
# encode the binary photo data to base64 to embed it in HTML
  encoded_photo = base64.b64encode(photo_data).decode('utf-8')
# create a data URI for the image which
# can be used as a source for the HTML image tag
  photo_src = f"data:image/*;base64,{encoded_photo}"
# close off cursor
  cursor.close()
# render the 'welcome.html' template, passing in the data
# from the form and the photo source for display
  return render_template('welcome.html',
first_name=first_name,
last_name=last_name,
photo_src=photo_src
)
# if the method is not POST -it is just a GET request90 # render and return the registration form
 return render_template('register.html')
@myapp.route('/logout')
def logout():
    global logged_in_user
    logged_in_user = "Guest"
    return render_template('home.html', user=logged_in_user)

@myapp.route('/vieworcreatealbum')
def vieworcreatealbum():
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM flusers WHERE email = %s', (logged_in_user,))
    userid = cursor.fetchone()
    cursor.execute('SELECT alname, doc FROM albums WHERE useri = %s', (userid,))
    albums_data = cursor.fetchall()
    albums_list = []
    for album in albums_data:
        alname, doc = album
        albums_list.append({
        'alname': alname,
        'doc': doc
        })
    cursor.close()
    return render_template('vieworcreatealbum.html', albums=albums_list)

@myapp.route('/createalbum', methods=['GET', 'POST'])
def createalbum():
    if request.method == 'POST' and logged_in_user != "Guest":
        albumname = request.form['alname']
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM flusers WHERE email = %s', (logged_in_user,))
        userid = cursor.fetchone()
        insert_command = """
        INSERT INTO albums (userid, alname, doc)
        VALUES (%s, %s, CURRENT_DATE)
        """;
        print(userid);
        insert_data = (userid, albumname);
        cursor.execute(insert_command, insert_data);
        conn.commit()
        cursor.close()
        return vieworcreatealbum()
    return render_template('createalbum.html')
# route that helps display all users
@myapp.route('/users')
def users():
    # create a cursor on the psql connection to execute SQL statement(s)
    cursor = conn.cursor()
    # execute a SELECT command to fetch all user data
    cursor.execute('SELECT fname, lname, email, photo, dob FROM flusers')
    # retrieve all rows of results
    users_data = cursor.fetchall()
    # list to hold user data with encoded photos
    users_list = []
    # loop through every user data obtained with fetchall()
    for user in users_data:
        first_name, last_name, email, photo_data, dob = user
        # encode the binary photo data to base64 to embed in HTML
        encoded_photo = base64.b64encode(photo_data).decode('utf-8')
        # create a data URI for the image which
        # can be used as a source for the HTML image tag
        photo_src = f"data:image/*;base64,{encoded_photo}"
        # Append user data to the list, including the photo source
        users_list.append({
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'photo_src': photo_src,
        'dob': dob
        })
    # close the cursor to free up resources
    cursor.close()
    # render the 'users.html' template,
    # passing in the users list for display
    return render_template('users.html', users=users_list)
    # check if this script is run directly (not imported),
    # and if so, start the Flask application
if __name__ == '__main__':
 myapp.run(debug=True)