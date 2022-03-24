from ast import dump
from crypt import methods
from ctypes import util
from flask import Flask, flash, render_template, request
import os
import utils

app = Flask(__name__);
# Secret key is needed to use some Flask functions, let's generate a random one
app.config['SECRET_KEY'] = os.urandom(12);
app.config['UPLOAD_FOLDER'] = 'static/resources/imgs/';
@app.route('/')
def index():
    return render_template('index.html.jinja');

@app.route('/services-types', methods = ['POST', 'GET'])
def services_types():
    if(request.method == 'POST'):
        posted_service_type = request.form;
        if('add_service_type' in posted_service_type):
            utils.updateDb('INSERT INTO services_types (name, desc) VALUES (?, ?)', (posted_service_type['name'], posted_service_type['desc'],));
            flash(posted_service_type['name'] + " created successfully.");
        elif('update_service_type' in posted_service_type):
            utils.updateDb('UPDATE services_types SET name = ?, desc = ? WHERE id = ?', (posted_service_type['name'], posted_service_type['desc'], posted_service_type['id'],));
            flash(posted_service_type['name'] + " updated successfully.");
        elif('delete_service_type' in posted_service_type):
            utils.updateDb('DELETE from services_types WHERE id = ?', (posted_service_type['id'],));
    data_services_types = utils.getRowsFromDb('SELECT * from services_types');
    return render_template('services-types.html.jinja', data=data_services_types);

@app.route('/service-type/<id>')
def edit_service_type(id):
    data_service_type = utils.getRowFromDb('SELECT * from services_types WHERE id = ?', (id,));
    return render_template('edit-service-type.html.jinja', data=data_service_type);

@app.route('/add-service-type')
def add_service_type():
    return render_template('add-service-type.html.jinja');

@app.route('/resources', methods = ['POST', 'GET'])
def resources():
    if(request.method == 'POST'):
        posted_resource = request.form;
        if('add_resource' in posted_resource):
            utils.updateDb('INSERT INTO resources (name, desc, price) VALUES (?, ?, ?)', 
            (posted_resource['name'], posted_resource['desc'], posted_resource['price'],));
            flash(posted_resource['name'] + " created successfully.");
        elif('update_resource' in posted_resource):
            utils.updateDb('UPDATE resources SET name = ?, desc = ?, price = ? WHERE id = ?', 
            (posted_resource['name'], posted_resource['desc'], posted_resource['price'], posted_resource['id'],));
            flash(posted_resource['name'] + " updated successfully.");
        elif('delete_resource' in posted_resource):
            # Let's delete the rows from resource_per_service table that are bound to the resource we're deleting
            utils.updateDb('DELETE from resources_per_service WHERE resource_id = ?', (posted_resource['id'],));
            utils.updateDb('DELETE from resources WHERE id = ?', (posted_resource['id'],));
            flash("Resource with ID " + posted_resource['id'] + " deleted successfully.");
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
        requested_service = None
        if('add_service' in posted_service):
            utils.updateDb('INSERT INTO services (name, desc, service_type_id, starting_date, ending_date) VALUES (?, ?, ?, ?, ?)', 
            (posted_service['name'], posted_service['desc'], posted_service['service_type'], posted_service['starting_date'], posted_service['ending_date'],));
            requested_service = utils.getRowFromDb('SELECT id from services WHERE name = ?', (posted_service['name'],));
            for i in range(0, int(posted_service['different_resources_count'])):
                utils.updateDb('INSERT INTO resources_per_service (service_id, resource_id, quantity) VALUES (?, ?, ?)',
                (requested_service['id'], posted_service['resource_id_' + str(i)], posted_service['quantity_' + str(i)],));
            flash(posted_service['name'] + " added successfully.");
        elif('update_service' in posted_service):
            requested_service = utils.getRowFromDb('SELECT id from services WHERE name = ?', (posted_service['name'],));
            # Let's re-create all the resources_per_service rows used by the current service
            utils.updateDb('DELETE from resources_per_service WHERE service_id = ? ', (posted_service['id'],));
            for i in range(0, int(posted_service['different_resources_count'])):
                utils.updateDb('INSERT INTO resources_per_service (service_id, resource_id, quantity) VALUES (?, ?, ?)',
                (requested_service['id'], posted_service['resource_id_' + str(i)], posted_service['quantity_' + str(i)],));
            utils.updateDb('UPDATE services SET name = ?, desc = ?, service_type_id = ?, starting_date = ?, ending_date = ?) WHERE id = ?', 
            (posted_service['name'], posted_service['desc'], posted_service['service_type'], posted_service['starting_date'], posted_service['ending_date'], posted_service['id'],));
            flash(posted_service['name'] + " updated successfully.");
        elif('delete_service' in posted_service):
            utils.updateDb('DELETE from resources_per_service WHERE service_id = ?', (posted_service['id'],));
            utils.updateDb('DELETE from services WHERE id = ? ', (posted_service['id'],));
            flash("Service with ID " + posted_service['id'] + " deleted successfully.");
    data_services = utils.getRowsFromDb('SELECT * from services');
    data_services_types = utils.getRowsFromDb('SELECT * from services_types');
    return render_template('services.html.jinja', services=data_services, services_types=data_services_types);

@app.route('/service/<id>')
def edit_service(id):
    data_service = utils.getRowFromDb('SELECT * from services WHERE id = ?', (id,));
    data_resources = utils.getRowsFromDb('SELECT * from resources');
    data_resources_per_service = utils.getRowsFromDb('SELECT * from resources_per_service WHERE service_id = ?', 
    (id,));
    data_services_types = utils.getRowsFromDb('SELECT * from services_types');
    return render_template('edit-service.html.jinja', service=data_service, resources_per_service=data_resources_per_service, resources=data_resources, services_types=data_services_types);

@app.route('/add-service')
def add_service():
    data_resources = utils.getRowsFromDb('SELECT * from resources');
    data_services_types = utils.getRowsFromDb('SELECT * from services_types');
    return render_template('add-service.html.jinja', resources=data_resources, services_types=data_services_types);

@app.route('/catalog-services', methods = ['POST', 'GET'])
def catalog_services():
    data_catalogs = utils.getRowsFromDb('SELECT * from catalog_services');
    for data_catalog in data_catalogs:
        # A new key created to store the benefit (money from the sell - money from bought resources)
        data_catalog['benefit'] = data_catalog['price'] * (100 - data_catalog['discount_percentage'])/100
        # We need to parse resources per service to get the ID of the resources and their quantity
        data_resources_per_service = utils.getRowsFromDb('SELECT * from resources_per_service WHERE service_id = ?', (data_catalog['service_id'],));
        for data_resource_per_service in data_resources_per_service:
            # We need to parse the resources to get the price we paid them
            data_resources = utils.getRowsFromDb('SELECT * from resources WHERE id = ?', (data_resource_per_service['resource_id'],));
            for data_resource in data_resources:
                if(data_resource['id'] == data_resource_per_service['resource_id']):
                    data_catalog['benefit'] -= data_resource['price'] * data_resource_per_service['quantity'];
        # Let's troncate some decimals from the benefit
        data_catalog['benefit'] = float("{:.2f}".format(data_catalog['benefit']));
    if(request.method == 'POST'):
        posted_catalog = request.form;
        if('add_catalog_service' in posted_catalog):
            utils.updateDb('INSERT INTO catalog_services (service_id, starting_date, ending_date, discount_percentage, price) VALUES (?, ?, ?, ?, ?) ',
            (posted_catalog['service_id'],posted_catalog['starting_date'], posted_catalog['ending_date'], posted_catalog['discount_percentage'], posted_catalog['price'],));
            flash("Catalog for Service ID " + posted_catalog['service_id'] + " created successfully.");
        elif('update_catalog_service' in posted_catalog):
            utils.updateDb('UPDATE catalog_services SET service_id = ?, starting_date = ?, ending_date = ?, discount_percentage = ?, price = ? WHERE id = ?',
            (posted_catalog['service_id'],posted_catalog['starting_date'], posted_catalog['ending_date'], posted_catalog['discount_percentage'], posted_catalog['price'], posted_catalog['id'],));
            flash("Catalog for Service ID " + posted_catalog['service_id'] + " updated successfully.");
        elif('delete_catalog_service' in posted_catalog):
            utils.updateDb('DELETE from catalog_services WHERE id = ? ', (posted_catalog['id'],));
            flash("Catalog for Service ID " + posted_catalog['service_id'] + " deleted successfully.");
    return render_template('catalog-services.html.jinja', catalogs=data_catalogs);

@app.route('/catalog-service/<id>')
def edit_catalog_service(id):
    data_catalog = utils.getRowFromDb('SELECT * from catalog_services WHERE id = ?', (id,));
    data_services = utils.getRowsFromDb('SELECT id, name from services');
    return render_template('edit-catalog-service.html.jinja', data_catalog=data_catalog, data_services=data_services);

@app.route('/add-catalog-service')
def add_catalog_service():
    data = utils.getRowsFromDb('SELECT id, name, starting_date, ending_date FROM services');
    return render_template('add-catalog-service.html.jinja', services=data);