from flask import Flask, render_template
import random
import os

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
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)