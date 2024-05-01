from flask import Flask, render_template
import random
import os
from driver_pkg.driver import Lidar_BLUEPRINT

class Webvisual():
    def __init__(self) -> None:
        
        self.x_data=[]
        self.y_data=[]

template_dir = os.path.abspath('/home/deepracer/adr-class/driver_pkg/driver_pkg/templates')
app = Flask(__name__, template_folder=template_dir)
app.register_blueprint(Lidar_BLUEPRINT)


@app.route('/')
def home():
    return render_template('index.html')


app.config.update(
    DEBUG=True,
    SECRET_KEY='secret_',
    SESSION_COOKIE_SECURE=True,
    REMEMBER_COOKIE_SECURE=True)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)