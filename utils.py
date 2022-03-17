from flask import Flask, flash, request
import os
import sqlite3
import flask
import jinja2
from werkzeug.utils import secure_filename

def dictFactory(cursor, row) -> dict:
    """_summary_
    Used to redefine sql3_instance.row_factory
    Args:
        cursor (_type_): _description_
        row (_type_): _description_

    Returns:
        dict: _description_
    """
    d = {};
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx];
    return d;

def connectDb(path : str = 'db/konpyutaden.db') -> sqlite3.Connection:
    """_summary_

    Args:
        path (str, optional): Path to db. Defaults to 'db/konpyutaden.db'.

    Returns:
        sqlite3: Database connection
    """
    db = None;
    try:
        db = sqlite3.connect(path);
        db.row_factory = dictFactory;
    except Exception as err:
        flash("Can't connect do database " + err, 'error');
    return db;

def updateDb(request : str, values : tuple = None):
    """_summary_
    Update values in the SQLite database

    Args:
        request (str): SQL Request
        values (tuple, optional): Values to compare with the SQL request. Defaults to None.
    """
    try:
        db = connectDb();
        cursor = db.cursor();
        if(type(values) is tuple):
            cursor.execute(request, values);
        else:
            cursor.execute(request);
        db.commit();
        db.close();
    except Exception as err:
        flash("Can't execute SQL request " + err, 'error');

def getRowsFromDb(request : str, values : tuple = None) -> dict:
    """_summary_
    Args:
        request (str): SQL Request
        values (tuple, optional): Values to compare with the SQL request. Defaults to None.

    Returns:
        dict: The elements requested by the request
    """
    elementsFromDb : dict = None
    try:
        db = connectDb();
        cursor = db.cursor();
        if(type(values) is tuple):
            elementsFromDb = cursor.execute(request, values).fetchall();
        else:
            elementsFromDb = cursor.execute(request).fetchall();
        db.close();
    except Exception as err:
        flash("Can't execute SQL request " + err, 'error')
    return elementsFromDb;

def getRowFromDb(request : str, values : tuple = None) -> dict:
    """_summary_
    Args:
        request (str): SQL Request
        values (tuple, optional): Values to compare with the SQL request. Defaults to None.

    Returns:
        dict: The element requested by the request
    """
    elementFromDb : dict = None;
    try:
        db = connectDb()
        cursor = db.cursor()
        if(type(values) is tuple):
            elementFromDb = cursor.execute(request, values).fetchone();
        else:
            elementFromDb = cursor.execute(request).fetchone();
        db.close()
    except Exception as err:
        flash("Can't execute SQL request " + err, 'error')
    return elementFromDb

# Upload Section
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'};
""" Allowed types to store a file """

def allowedFile(filename : str):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS;

def uploadFile(requestFile, uploadPath = 'static/imgs/'):
    """Saves a file on the server

    Args:
        requestFile (_type_): A value from an <input type="file"> from a POST form, example : request.form['file']
        uploadPath (str, optional): _description_. Defaults to 'static/imgs/'.
    """
    file = requestFile
    filename = None
    if(file.filename == ''):
        pass
    if(file and allowedFile(file.filename)):
        filename = secure_filename(file.filename);
        file.save(os.path.join(uploadPath, filename));