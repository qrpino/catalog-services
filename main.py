from flask import Flask, render_template
import utils

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/resources/imgs/'
@app.route('/')
def index():
    return render_template('index.html.jinja')

@app.route('/services-types')
def services_types():
    data_services_types = utils.getRowsFromDb('SELECT * from services_types');
    return render_template('services-types.html.jinja', data=data_services_types);

@app.route('/service-type/<id>')
def edit_service_type(id):
    pass;

@app.route('/resources')
def resources():
    data_resources = utils.getRowsFromDb('SELECT * from resources');
    return render_template('resources.html.jinja', data=data_resources)

@app.route('/resource/<id>')
def edit_resource(id):
    pass;

@app.route('/services')
def services():
    data_services = utils.getRowsFromDb('SELECT * from services');
    return render_template('resources.html.jinja', data=data_services)

@app.route('/service/<id>')
def edit_service(id):
    pass;

@app.route('/catalog-services-prices')
def catalog_services_prices():
    pass;

@app.route('/catalog-service-price/<id>')
def edit_catalog_service_price(id):
    pass;
