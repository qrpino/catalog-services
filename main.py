from crypt import methods
from ctypes import util
from flask import Flask, flash, render_template, request
import os
import utils

app = Flask(__name__)
# Secret key is needed to use some Flask functions, let's generate a random one
app.config['SECRET_KEY'] = os.urandom(12)
app.config['UPLOAD_FOLDER'] = 'static/resources/imgs/'
@app.route('/')
def index():
    return render_template('index.html.jinja')

@app.route('/services-types', methods = ['POST', 'GET'])
def services_types():
    if(request.method == 'POST'):
        posted_service_type = request.form
        if('add_service_type' in posted_service_type):
            utils.updateDb('INSERT INTO services_types (name, desc) VALUES (?, ?)', (posted_service_type['name'], posted_service_type['desc'],))
    data_services_types = utils.getRowsFromDb('SELECT * from services_types');
    return render_template('services-types.html.jinja', data=data_services_types);

@app.route('/service-type/<id>')
def edit_service_type(id):
    data_service_type = utils.getRowFromDb('SELECT * from services_types WHERE id = ?', (id,));
    return render_template('edit-service-type.html.jinja', data=data_service_type);

@app.route('/add-service-type')
def add_service_type():
    return render_template('add-service-type.html.jinja')

@app.route('/resources', methods = ['POST', 'GET'])
def resources():
    if(request.method == 'POST'):
        posted_resource = request.form
        if('add_resource' in posted_resource):
            utils.updateDb('INSERT INTO resources (name, desc, price) VALUES (?, ?, ?)', (posted_resource['name'], posted_resource['desc'], posted_resource['price'],));
        elif('update_resource' in posted_resource):
            pass;
        # flash(resource['desc'] updated successfuly)
    data_resources = utils.getRowsFromDb('SELECT * from resources');
    return render_template('resources.html.jinja', data=data_resources);

@app.route('/resource/<id>')
def edit_resource(id):
    data_resource = utils.getRowFromDb('SELECT * from resources WHERE id = ?', (id,));
    return render_template('edit-resource.html.jinja', data=data_resource);

@app.route('/add-resource')
def add_resource():
    return render_template('add-resource.html.jinja');

@app.route('/services', methods = ['POST', 'GET'])
def services():
    if(request.method == 'POST'):
        posted_service = request.form;
        if('add_service' in posted_service):
            utils.updateDb('INSERT INTO services (name, desc, service_type_id, starting_date, ending_date) VALUES (?, ?, ?, ?, ?)', 
            (posted_service['name'], posted_service['desc'], posted_service['service_type_id'], posted_service['starting_date'], posted_service['ending_date'],));
            service_id = utils.getRowFromDb('SELECT id from services WHERE name = ?', (posted_service['name'],));
            for i in range(posted_service['different_resources_count'] + 1):
                utils.updateDb('INSERT INTO resources_per_service (service_id, resource_id, quantity) VALUES (?, ?, ?)',
                (service_id, posted_service['resource_id_' + str(i)], posted_service['quantity_' + str(i)],));

    data_services = utils.getRowsFromDb('SELECT * from services');
    return render_template('services.html.jinja', data=data_services);

@app.route('/service/<id>')
def edit_service(id):
    data = {'service' : utils.getRowFromDb('SELECT * from services WHERE id = ?', (id,)),
    'resources' : utils.getRowsFromDb('SELECT * from resources_per_service WHERE service_id = ?', (id,))};
    return render_template('edit-service.html.jinja', data=data);

@app.route('/add-service')
def add_service():
    data = {"resources" : utils.getRowsFromDb('SELECT * from resources'),
    "services_types" : utils.getRowsFromDb('SELECT * from services_types')};
    return render_template('add-service.html.jinja', resources=data['resources'], services_types=data['services_types']);

@app.route('/catalog-services-prices')
def catalog_services_prices():
    pass;

@app.route('/catalog-service-price/<id>')
def edit_catalog_service_price(id):
    pass;
