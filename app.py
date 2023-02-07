from flask import Flask, render_template
from views import views

app = Flask(__name__)
# the url prefix means we will access the function in the views route
# defined in the views file with the prefix views
# create a cache instance

app.register_blueprint(views, url_prefix="/views")
 
if __name__ == "__main__": 
    app.run(debug=False, port=8080)