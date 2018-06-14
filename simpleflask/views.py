from flask import (Blueprint, flash, g, redirect, render_template, request,
                   url_for)
from werkzeug.exceptions import abort
from simpleflask.db import get_db


bp = Blueprint('views', __name__)


@bp.route('/')
def index():
    page_title = 'Index'
    
    db = get_db()
    entries = db.execute(
        'SELECT e.id, author, created, title, body'
        ' FROM entry e'
        ' ORDER BY created DESC'
    ).fetchall()

    return render_template(
        'index.html',
        entries=entries,
        page_title=page_title)

@bp.route('/add', methods=('GET', 'POST'))
def add():
    page_title = 'Add Entry'

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        author = request.form['author']
        error = None
    
        if not title:
            error = 'Title is required.'
        
        if not author:
            error = 'Author is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO entry (title, body, author)'
                ' VALUES (?, ?, ?)',
                (title, body, author)
            )
            db.commit()
            return redirect(url_for('index'))

    return render_template('add.html', page_title=page_title)


def get_entry(id):
    entry = get_db().execute(
        'SELECT e.id, title, body, created, author'
        ' FROM entry e'
        ' WHERE e.id = ?', (id,)
    ).fetchone()

    if entry is None:
        abort(404, "Entry id {0} doesn't exist.".format(id))

    return entry


@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    page_title = 'Edit Entry'

    entry = get_entry(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        author = request.form['author']
        error = None

        if not title:
            error = 'Title is required.'

        if not author:
            error = 'Author is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE entry SET title = ?, body = ?, author = ?'
                ' WHERE id = ?',
                (title, body, author, id)
            )
            db.commit()
            return redirect(url_for('index'))

    return render_template('edit.html', entry=entry)


@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    get_entry(id)
    db = get_db()
    db.execute('DELETE FROM entry WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('index'))
