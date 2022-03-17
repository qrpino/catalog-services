from flask import Flask, render_template
import utils

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/resources/imgs/'
@app.route('/')
def index():
    return render_template('index.html.jinja', data = None);

@app.route('/modify-product')
def modify_product():
    pass;