import pickle
import os 
from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import random

login_page=''''<html>
        <head>
        </head>
        <body>
        <h1>Please Login</h1>
            <form action="http://localhost:8000/login" method="post">
            <input type="text" name="username">
            <input type="text" name="password">
            <input type="submit">
            </form>
        </body>
    </html>'''
sign_up_page='''<html>
        <head>
        </head>
        <body>
        <h1>Please sign up</h1>
            <form action="http://localhost:8000/sign_up" method="post">
            <input type="text" name="username">
            <input type="text" name="password">
            <input type="submit">
            </form>
        </body>
    </html>'''
 
# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        
        # Send response status code
        self.send_response(200)
 
        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()
 
        # Write content as utf-8 data

        if self.path == "/login":
            self.wfile.write(bytes(login_page, "utf8"))

        if self.path == "/sign_up":
            self.wfile.write(bytes(sign_up_page, 'utf8'))

        return

    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
        if ctype == 'multipart/form-data':
            postvars = cgi.parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers.get('content-length'))
            postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
        else:
            postvars = {}

        self.send_response(200)
 
        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()


        if self.path=="/login": #Submit click response object on primary page
            val=check(str(postvars[b"username"]), str(postvars[b"password"]))
            if val=="Retry Password":
                self.wfile.write(bytes(login_page, "utf8"))

            if val=="sign up":
                self.wfile.write(bytes(sign_up_page, "utf8"))

            if val=="Validated":
                print("nani")
                self.wfile.write(bytes('''<html>
        <head>
        </head>
        <body>
        <h1>Approved</h1>
        </body>
    </html>''', "utf8"))

            else:
                self.wfile.write(bytes(val, "utf8"))

        if self.path=="/sign_up": #Submit click response object on login page
            val=setup(str(postvars[b"username"]), str(postvars[b"password"]))
            if val=="Enter a password":
                self.wfile.write(bytes(sign_up_page, "utf8"))

            if val=="Login please":
                self.wfile.write(bytes(login_page, "utf8"))

        

    
def check(username, password):
#checks to see if user is in database. Either redirects to webpage/sends SMS to display pin or login page
    pickle_in=open('Database.pickle', 'rb')
    users=pickle.load(pickle_in)
    if username in users:
        if len(users[username])==2:
            password=str(password)[3:7]
            if users[username][1]==password:
                print("jack")
                pickle_in.close()
                return "Validated"
        if users[username][0]==password:
            pin=''
            for i in range(4):
                pin+=str(random.randint(1,4))
            
            users[username].append(pin)
            pickle_in.close()
            pickle_out=open('Database.pickle', 'wb') 
            pickle.dump(users, pickle_out) #add new user
            pickle_in.close()
            return pin
        else: #asks to Retry password
            pickle_in.close()  
            return "Retry Password"

    else: 
        return "sign up"

def setup(username, password):
    pickle_in=open('Database.pickle', 'rb')
    users=pickle.load(pickle_in)

    if password=="":
        pickle_in.close()
        return "Enter a password"

    else:
        users[username]=[]
        users[username].append(password)
        pickle_in.close()
        pickle_out=open('Database.pickle', 'wb') 
        pickle.dump(users, pickle_out) #add new user
        pickle_in.close() #close the file again
        return "Login please" #go back to 1st page
    

def run():
  print('starting server...')

  # Choose port 8080, for port 80, which is normally used for a http server, you need root access
  server_address = ('127.0.0.1', 8000)
  httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
  print('running server...')
  httpd.serve_forever()
 
 
run()