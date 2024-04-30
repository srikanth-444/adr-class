from flask import Flask, render_template
import random
import os
from flask_cors import CORS

x_data=[]
y_data=[]

template_dir = os.path.abspath('~/adr-class/driver_pkg/driver_pkg/webVisuals/templates')
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/lidar', methods=["GET", "POST"])
def lidar():
    data ={
            "x":x_data,
            "y":y_data
        }
    return data
app.config.update(
    DEBUG=True,
    SECRET_KEY='secret_',
    SESSION_COOKIE_SECURE=True,
    REMEMBER_COOKIE_SECURE=True)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)