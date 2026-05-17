from flask import Flask
# Import the Flask class from the flask module.
myapp = Flask(__name__)
# Creating an instance of the Flask class named myapp.
@myapp.route('/')
# The @myapp.route('/') decorator defines the 'route' of the application.
# If a user visits the default 127.0.0.1 IP at port 5000,
# then Flask will call the function defined just below:
def ciao_k29(): # put application's code here
 print("\n>>> Development Web Server in Operation <<< \n");
 print("The function ciao_k29() found on the route gets executed every time \n");
 return '<p> Hello! \
 <p> &rarr; This is the K29-Section of \
 the Odd-Matriculation IDed Students.\
 <br> &rarr; The home page of the class is at \
 <i>https://www.alexdelis.eu/k29</i> \
 <p>Have a good day!<p>\
 ';
if __name__ == '__main__':
 myapp.run()