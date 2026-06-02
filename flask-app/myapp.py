# import necessary libraries from Flask,
# psycopg2 for PSQL, and base64 for encoding
from flask import Flask, request, render_template, make_response, redirect, url_for
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
@myapp.route('/addfriendimmediate', methods=['POST'])
def addfriendimmediate():
    email = request.form.get('email')
    cursor = conn.cursor()
    cursor.execute('SELECT fname, lname, email FROM flusers WHERE email = %s', (email,))
    existing_friend = cursor.fetchone()
    first_name = existing_friend[0]
    last_name = existing_friend[1]
    cursor.execute('SELECT id FROM flusers WHERE email = %s', (logged_in_user,))
    userid = cursor.fetchone()
    insert_command = """
    INSERT INTO flfriends (fid, fname, lname, email)
    VALUES (%s, %s, %s, %s)
    """;
    insert_data = (userid, first_name, last_name, email);
    cursor.execute(insert_command, insert_data);
    conn.commit()
    cursor.close()
    return render_template('home.html', user=logged_in_user)
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
    if logged_in_user == "Guest":
        return "Please log in to view your friends."
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
    if logged_in_user == "Guest":
        return "Please log in to view your albums."
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM flusers WHERE email = %s', (logged_in_user,))
    userid = cursor.fetchone()
    cursor.execute('SELECT alname, doc, albumid FROM albums WHERE userid = %s', (userid,))
    albums_data = cursor.fetchall()
    albums_list = []
    for album in albums_data:
        alname, doc, albumid = album
        albums_list.append({
        'alname': alname,
        'doc': doc,
        'albumid': albumid
        })
    cursor.close()
    return render_template('vieworcreatealbum.html', albums=albums_list)
@myapp.route('/viewuseralbums')
def viewuseralbums():
    email = request.args.get('email')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM flusers WHERE email = %s', (email,))
    userid = cursor.fetchone()
    cursor.execute('SELECT alname, doc, albumid FROM albums WHERE userid = %s', (userid,))
    albums_data = cursor.fetchall()
    albums_list = []
    for album in albums_data:
        alname, doc, albumid = album
        albums_list.append({
        'alname': alname,
        'doc': doc,
        'albumid': albumid
        })
    cursor.close()
    return render_template('viewuseralbums.html', albums=albums_list, email=email)
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
@myapp.route('/viewalbumphotos')
def viewalbumphotos():
    albumid = request.args.get('albumid')
    print("albumid: ", albumid)
    cursor = conn.cursor()
    cursor.execute('SELECT alname, userid FROM albums WHERE albumid = %s', (albumid,))
    album_row = cursor.fetchone()
    alname, owner_id = album_row
    cursor.execute('SELECT id FROM flusers WHERE email = %s', (logged_in_user,))
    user_id = cursor.fetchone()[0] if logged_in_user != "Guest" else None
    can_add = (user_id == owner_id)
    print("owner_id: ", owner_id)
    print("user_id: ", user_id)
    cursor.execute('SELECT phdata, doc, phname, photoid FROM photos WHERE albumid = %s', (albumid,))
    photos = cursor.fetchall()
    photos_list = []
    for photo in photos:
        photo_data, doc, phname, photoid = photo
        encoded_photo = base64.b64encode(photo_data).decode('utf-8')
        photo_src = f"data:image/*;base64,{encoded_photo}"
        cursor.execute('SELECT COUNT(*) FROM likes WHERE photoid = %s', (photoid,))
        phlikes = cursor.fetchone()[0]
        cursor.execute('SELECT EXISTS (SELECT 1 FROM likes WHERE userid = %s AND photoid = %s)', (user_id, photoid))
        is_liked = cursor.fetchone()[0]
        heart_icon = url_for('static', filename='heart.png' if is_liked else 'unheart.png')
        cursor.execute('SELECT flusers.fname, flusers.lname FROM likes JOIN flusers ON likes.userid = flusers.id WHERE likes.photoid = %s', (photoid,))
        likers_data = cursor.fetchall()
        likers_list = []
        for liker in likers_data:
            liker_fname, liker_lname = liker
            likers_list.append({
                'first_name': liker_fname,
                'last_name': liker_lname
            })
        cursor.execute('SELECT t.tagname FROM tags t JOIN phototags pt ON t.tagid = pt.tagid WHERE pt.photoid = %s', (photoid,))
        tags = cursor.fetchall()
        tag_list=[]
        for tag in tags:
          tag_list.append(tag[0])
        photos_list.append({
        'photo_src': photo_src,
        'doc': doc,
        'name': phname,
        'photoid': photoid,
        'phlikes': phlikes,
        'liked': is_liked,
        'likers': likers_list,
        'heart_icon': heart_icon,
        'tags' : tag_list
        })
    cursor.close()
    return render_template('viewalbumphotos.html', photos=photos_list, alname=alname, albumid=albumid, current_user=logged_in_user, can_add=can_add)
@myapp.route('/deletealbum', methods=['POST'])
def deletealbum():
    if request.method == 'POST':
        albumid = request.form.get('albumid')
        cursor = conn.cursor()
        cursor.execute('SELECT photoid FROM photos WHERE albumid = %s', (albumid,))
        photoids = cursor.fetchall()
        for photoid in photoids:
            cursor.execute('DELETE FROM comments WHERE photoid = %s', (photoid[0],))
            cursor.execute('DELETE FROM likes WHERE photoid = %s', (photoid[0],))
        cursor.execute('DELETE FROM photos WHERE albumid = %s', (albumid,))
        delete_command = """
        DELETE FROM albums
        WHERE albumid = %s
        """;
        delete_data = (albumid,);
        cursor.execute(delete_command, delete_data);
        conn.commit()
        cursor.close()
        return redirect(url_for('vieworcreatealbum')) #online help
@myapp.route('/removephoto', methods=['POST'])
def removephoto():
    if request.method == 'POST':
        photoid = request.form.get('photoid')
        albumid = request.form.get('albumid')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM comments WHERE photoid = %s', (photoid,))
        cursor.execute('DELETE FROM likes WHERE photoid = %s', (photoid,))
        delete_command = """
        DELETE FROM photos
        WHERE photoid = %s
        """;
        delete_data = (photoid,);
        cursor.execute(delete_command, delete_data);
        conn.commit()
        cursor.close()
        return redirect(url_for('viewalbumphotos', albumid=albumid)) #online help
@myapp.route('/addphoto', methods=['GET', 'POST'])
def addphoto():
    if request.method == 'POST':
        albumid = request.form.get('albumid') or albumid
    if request.method == 'POST' and logged_in_user != "Guest":
        cursor = conn.cursor()
        photo = request.files['photo'].read()
        name = request.form['name']
        tags_text = request.form.get('tags','')
        tag_list = tags_text.split()
        cursor = conn.cursor()
        insert_command = """
        INSERT INTO photos (albumid, phdata, phname, doc)
        VALUES (%s, %s, %s, CURRENT_DATE)
        """
        insert_data = (albumid, psycopg2.Binary(photo), name)
        cursor.execute(insert_command, insert_data)
        cursor.execute('SELECT photoid FROM photos WHERE albumid= %s AND phname= %s ORDER BY photoid DESC LIMIT 1', (albumid, name))
        photoid = cursor.fetchone()[0]
        for tagname in tag_list:
          cursor.execute('SELECT tagid FROM tags WHERE tagname = %s', (tagname,))
          row = cursor.fetchone()
          if row :
            tagid = row[0]
          else:
            cursor.execute('INSERT INTO tags (tagname) VALUES (%s)', (tagname,))
            cursor.execute('SELECT tagid FROM tags WHERE tagname = %s', (tagname,))
            tagid = cursor.fetchone()[0]
          cursor.execute('INSERT INTO phototags (photoid, tagid) VALUES (%s, %s)', (photoid, tagid))
        conn.commit()
        cursor.close()
        return redirect(url_for('viewalbumphotos', albumid=albumid)) #online help
    albumid = request.args.get('albumid')
    cursor = conn.cursor()
    cursor.execute('SELECT alname FROM albums WHERE albumid = %s', (albumid,))
    alname = cursor.fetchone()[0]
    print("alname: ", alname)
    cursor.close()
    return render_template('addphoto.html', albumid=albumid, alname=alname)
@myapp.route('/likephoto', methods=['POST'])
def likephoto():
  if logged_in_user == "Guest":
    return "Please log in to like photos."
  if request.method == 'POST':
    photoid = request.form.get('photoid')
    albumid = request.form.get('albumid')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM flusers WHERE email = %s', (logged_in_user,))
    print("logged_in_user: ", logged_in_user)
    userid = cursor.fetchone()[0]
    print("userid: ", userid)
    cursor.execute('SELECT EXISTS (SELECT 1 FROM likes WHERE userid = %s AND photoid = %s)', (userid, photoid))
    if cursor.fetchone()[0]:
        delete_command = """
        DELETE FROM likes
        WHERE userid = %s AND photoid = %s
        """;
        delete_data = (userid, photoid);
        cursor.execute(delete_command, delete_data);
        heart = url_for('static', filename='unheart.png')
    else:
        insert_command = """
        INSERT INTO likes (userid, photoid)
        VALUES (%s, %s)
        """;
        insert_data = (userid, photoid);
        cursor.execute(insert_command, insert_data);
        heart = url_for('static', filename='heart.png')
    print("userid: ", userid)
    print("photoid: ", photoid)
    conn.commit()
    cursor.close()
    return redirect(url_for('viewalbumphotos', albumid=albumid, heart=heart)) #online help
@myapp.route('/viewcomments')
def viewcomments():
    photoid = request.args.get('photoid')
    cursor = conn.cursor()
    cursor.execute('SELECT phname FROM photos WHERE photoid = %s', (photoid,))
    photoname = cursor.fetchone()[0]
    cursor.execute('SELECT phdata FROM photos WHERE photoid = %s', (photoid,))
    photo_data = cursor.fetchone()[0]
    encoded_photo = base64.b64encode(photo_data).decode('utf-8')
    photo_src = f"data:image/*;base64,{encoded_photo}"    
    cursor.execute('SELECT comments.userid, comments.photoid, comments.comment, comments.doc FROM comments WHERE comments.photoid = %s', (photoid,))
    comments_data = cursor.fetchall()
    comments_list = []
    for comment in comments_data:
        userid, photoid, comment_text, doc = comment
        cursor.execute('SELECT fname, lname FROM flusers WHERE id = %s', (userid,))
        commenter_data = cursor.fetchone()
        commenter_fname, commenter_lname = commenter_data if commenter_data else ("Guest", "User")
        comments_list.append({
            'first_name': commenter_fname,
            'last_name': commenter_lname,
            'comment_text': comment_text
        })
    cursor.close()
    return render_template('viewcomments.html', comments=comments_list, photoname=photoname, photoid=photoid, photo_src=photo_src)
@myapp.route('/addcomment', methods=['POST'])
def addcomment():
  if request.method == 'POST':
    photoid = request.form.get('photoid')
    albumid = request.form.get('albumid')
    comment_doc = request.form.get('comment_text')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM flusers WHERE email = %s', (logged_in_user,))
    userid = cursor.fetchone()[0] if logged_in_user != "Guest" else None
    insert_command = """
    INSERT INTO comments (userid, photoid, comment, doc)
    VALUES (%s, %s, %s, CURRENT_DATE)
    """;
    insert_data = (userid, photoid, comment_doc);
    cursor.execute(insert_command, insert_data);
    conn.commit()
    cursor.close()
    return redirect(url_for('viewcomments', photoid=photoid, albumid=albumid)) #online help
@myapp.route('/searchcomments' , methods=['GET', 'POST'])
def searchcomments():
    if request.method == 'POST':
        search_query = request.form.get('search_query')
        cursor = conn.cursor()
        cursor.execute("""
        SELECT comments.comment, flusers.fname, flusers.lname, photos.phname, photos.phdata
        FROM comments
        JOIN flusers ON comments.userid = flusers.id
        JOIN photos ON comments.photoid = photos.photoid
        WHERE comments.comment = %s
        """, (search_query,))
        search_results_data = cursor.fetchall()
        search_results_list = []
        for result in search_results_data:
            comment_text, commenter_fname, commenter_lname, phototitle, photo_data = result
            encoded_photo = base64.b64encode(photo_data).decode('utf-8')
            photo_src = f"data:image/*;base64,{encoded_photo}"
            search_results_list.append({
                'comment_text': comment_text,
                'commenter_fname': commenter_fname,
                'commenter_lname': commenter_lname,
                'phototitle': phototitle,
                'photo_src': photo_src
            })
        cursor.close()
        return render_template('searchcommentsresults.html', search_results=search_results_list, search_query=search_query)
    return render_template('searchcomments.html', search_results=None)
@myapp.route('/useractivity')
def useractivity():
    cursor = conn.cursor()
    query = """
    SELECT 
        u.id,
        u.fname,
        u.lname,
        COALESCE(photo_count, 0) as photos_uploaded,
        COALESCE(comment_count, 0) as comments_on_others,
        COALESCE(photo_count, 0) + COALESCE(comment_count, 0) as total_activity
    FROM flusers u
    LEFT JOIN (
        SELECT userid, COUNT(*) as photo_count
        FROM photos
        JOIN albums ON photos.albumid = albums.albumid
        GROUP BY userid
    ) photos_uploaded ON u.id = photos_uploaded.userid
    LEFT JOIN (
        SELECT c.userid, COUNT(*) as comment_count
        FROM comments c
        JOIN photos p ON c.photoid = p.photoid
        JOIN albums a ON p.albumid = a.albumid
        WHERE c.userid != a.userid
        GROUP BY c.userid
    ) comments_on_others ON u.id = comments_on_others.userid
    ORDER BY total_activity DESC
    LIMIT 10;
    """
    cursor.execute(query)
    activity_data = cursor.fetchall()
    
    activity_list = []
    for row in activity_data:
        activity_list.append({
            'id': row[0],
            'fname': row[1],
            'lname': row[2],
            'photos_uploaded': row[3],
            'comments_on_others': row[4],
            'total_activity': row[5]
        })
    
    cursor.close()
    return render_template('useractivity.html', activities=activity_list)
# route that helps display all users
@myapp.route('/friendsoffriends')
def friendsoffriends():
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM flusers WHERE email = %s', (logged_in_user,))
    userid = cursor.fetchone()
    cursor.execute('SELECT email FROM flfriends WHERE fid = %s', (userid[0],))
    friends_emails = cursor.fetchall()
    friends_of_friends_list = []
    for friend_email in friends_emails:
        cursor.execute('SELECT id FROM flusers WHERE email = %s', (friend_email[0],))
        friend_id = cursor.fetchone()
        cursor.execute('SELECT email FROM flfriends WHERE fid = %s', (friend_id[0],))
        friends_of_friend_emails = cursor.fetchall()
        for fof_email in friends_of_friend_emails:
            if fof_email != logged_in_user:
                cursor.execute('SELECT fname, lname FROM flusers WHERE email = %s', (fof_email[0],))
                fof_data = cursor.fetchone()
                fof_fname, fof_lname = fof_data if fof_data else ("Unknown", "User")
                friends_of_friends_list.append({
                    'first_name': fof_fname,
                    'last_name': fof_lname,
                    'email': fof_email[0]
                })
    cursor.close()
    return render_template('friendsoffriends.html', friends_of_friends=friends_of_friends_list)
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
        'email': email, #pythonemail=request.arg.get('email)
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
@myapp.route('/addtag', methods=[ 'POST' ])
def addtag():
  if logged_in_user == "Guest":
    return "Please log in first to add tag"
  photoid = request.form['photoid']
  tagname = request.form['tagname']
  cursor = conn.cursor()
  cursor.execute(' INSERT INTO tags (tagname) VALUES (%s)', (tagname,)) #insert tag 
  cursor.execute(' SELECT tagid FROM tags WHERE tagname = %s', (tagname,)) #get tagid
  row = cursor.fetchone()
  if row:
    tagid= row[0]
  else:
    cursor.execute('INSERT INTO tags (tagname) VALUES (%s) RETURNING tagid', (tagname,))
    tagid= cursor.fetchone()[0]
  cursor.execute('INSERT INTO phototags (photoid, tagid) VALUES (%s, %s)', (photoid, tagid)) #link tag w photo
  conn.commit()
  cursor.close()
  return redirect(url_for('viewalbumphotos', albumid=request.form.get('albumid')))
@myapp.route('/tag/<tagname>')
def viewphotosbytag(tagname):
  mode = request.args.get('mode', 'all')
  cursor = conn.cursor()
  if mode == "my":
    cursor.execute("""SELECT p.photoid, p.phdata, p.phname, p.doc FROM photos p 
    JOIN phototags pt ON p.photoid = pt.photoid JOIN tags t ON t.tagid = pt.tagid
    JOIN albums a ON p.albumid = a.albumid JOIN flusers u ON a.userid = u.id
    WHERE t.tagname = %s AND u.email = %s""", (tagname, logged_in_user))
  else:
    cursor.execute("""SELECT p.photoid, p.phdata, p.phname, p.doc FROM photos p 
    JOIN phototags pt ON p.photoid = pt.photoid JOIN tags t ON t.tagid = pt.tagid
    WHERE t.tagname = %s""", (tagname,))
  photos = cursor.fetchall()
  cursor.close()
  photos_list=[]
  for photo in photos:
    photoid, photodata, name, doc= photo
    encoded_photo = base64.b64encode(photodata).decode('utf-8')
    photos_list.append({
      "photo_src": f"data:image/*;base64,{encoded_photo}",
      "name": name, 
      "photoid": photoid
    })
  return render_template("tagphotos.html", photos=photos_list, tag=tagname, mode=mode)
@myapp.route('/populartags')
def populartags():
  cursor = conn.cursor()
  cursor.execute(""" SELECT t.tagname, COUNT(*) as popularity FROM tags t
  JOIN phototags pt ON t.tagid = pt.tagid GROUP BY t.tagname ORDER BY popularity DESC""")
  tags = cursor.fetchall()
  cursor.close()
  return render_template("populartags.html", tags=tags)
@myapp.route('/searchtag')
def searchtag():
  search = request.args.get('search','')
  tag_list= search.split()
  cursor = conn.cursor()
  cursor.execute(""" SELECT p.photoid, p.phdata, p.phname, COUNT(t.tagid) AS matchct FROM photos p
  JOIN phototags pt ON p.photoid = pt.photoid JOIN tags t ON pt.tagid = t.tagid
  WHERE t.tagname = ANY(%s) GROUP BY p.photoid, p.phdata, p.phname ORDER BY matchct DESC""", 
  (tag_list,))
  photos = cursor.fetchall()
  cursor.close()
  photos_list=[]
  for photo in photos:
    photoid, photodata, name, matchct= photo
    encoded_photo = base64.b64encode(photodata).decode('utf-8')
    photo_src = f"data:image/*;base64,{encoded_photo}"
    photos_list.append({
      "photoid": photoid,
      "photo_src": photo_src,
      "name": name
    })
  return render_template("searchtags.html", photos= photos_list)
if __name__ == '__main__':
 myapp.run(debug=True)