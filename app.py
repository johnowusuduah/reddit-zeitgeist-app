from flask import Flask, render_template
from views import views

# HTTP METHODS EXPLANATION
# 1. GET: Used to send and receive data in an insecure manner and is visible to anyone
# 2. POST: Used to send and receive data that is encrypted and cannot be seen from either end and is not
#          stored on the web server.


app = Flask(__name__)
# the url prefix means we will access the function in the views route
# defined in the views file with the prefix views
app.register_blueprint(views, url_prefix="/views")
 

if __name__ == "__main__": 
    app.run(debug=True)