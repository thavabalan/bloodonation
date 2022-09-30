from distutils.log import error
import functools
from pickle import NONE
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from apphello.db import get_db

bp = Blueprint('register', __name__, url_prefix='/register')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        name = request.form['name']
        id = request.form['donorid']
        group = request.form['bgroup']
        gender = request.form['gender']
        age = request.form['age']
        idnum = request.form['id']
        contact = request.form['contact']
        address = request.form['address']
        recurrent = request.form['recurrent']
        agree = request.form['agree']
        db = get_db()
        error = None

        if not name:
            error = 'Name is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO donors (dname, donorid, donorgroup, dgender, dage, did, dcontact, daddress, recurrent, agree) VALUES (?, ?, ?, ? ,? ,? ,?, ?,?,?)",
                    (name,id,group,gender,age,idnum,contact,address,recurrent,agree),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                flash('Success Fully Registered.', 'success')

                return redirect(url_for("register.register"))

        flash(error,'danger')

    return render_template('register/register.html')

@bp.route('/list', methods=('GET', 'POST'))
def list():
    db = get_db()
    error = None
    donors = db.execute(
        "select * from donors"
    ).fetchall()
    return render_template('register/list.html',donors=donors)
@bp.route('/<int:id>/delete', methods=('GET',))
def delete(id):
    db = get_db()
    db.execute('DELETE FROM donors WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('register.list'))
