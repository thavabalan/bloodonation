
import os
import os.path
import sqlite3
from apphello.db import get_db

from flask import Flask, Response,render_template



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/', methods=['GET'])
    def metrics():  # pragma: no cover
        db = get_db()
        error = None
        totaldonors = db.execute(
        "select COUNT(id) from donors"
    ).fetchone()[0]
        totalvolume = format(totaldonors*450,',d')
        male = db.execute(
            "select COUNT(id) from donors where dgender = 'Male'"
        ).fetchone()[0]
        female = db.execute(
            "select COUNT(id) from donors where dgender = 'Female'"
        ).fetchone()[0]
        recurrent = db.execute(
            "select COUNT(id) from donors where recurrent = 1"
        ).fetchone()[0]
        ap = db.execute(
            "select COUNT(id) from donors where donorgroup = 'A+'"
        ).fetchone()[0]
        an = db.execute(
            "select COUNT(id) from donors where donorgroup =  'A-'"
        ).fetchone()[0]
        bp = db.execute(
            "select COUNT(id) from donors where donorgroup =  'B+'"
        ).fetchone()[0]
        bn = db.execute(
            "select COUNT(id) from donors where donorgroup =  'B-'"
        ).fetchone()[0]
        op = db.execute(
            "select COUNT(id) from donors where donorgroup =  'O+'"
        ).fetchone()[0]
        on = db.execute(
            "select COUNT(id) from donors where donorgroup =  'O-'"
        ).fetchone()[0]
        abp = db.execute(
            "select COUNT(id) from donors where donorgroup = 'AB+'"
        ).fetchone()[0]
        abn = db.execute(
            "select COUNT(id) from donors where donorgroup =  'AB-'"
        ).fetchone()[0]
        age1 = db.execute(
            "select COUNT(id) from donors where dage BETWEEN 18 AND 35"
        ).fetchone()[0]
        age2 = db.execute(
            "select COUNT(id) from donors where dage BETWEEN 35 AND 45"
        ).fetchone()[0]
        age3 = db.execute(
            "select COUNT(id) from donors where dage BETWEEN 45 AND 65"
        ).fetchone()[0]
        return render_template('index.html',totalvolume = totalvolume,recurrent=recurrent,age1 = age1,age2=age2,age3=age3,totaldonors = totaldonors,male = male,female = female,ap=ap,an=an,bp=bp,bn=bn,op=op,on=on,abp=abp,abn=abn)
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    from . import db
    db.init_app(app)
    from . import register
    app.register_blueprint(register.bp)
    return app
