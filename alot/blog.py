from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,current_app
)

from werkzeug.exceptions import abort

from alot.auth import login_required
from alot.db import get_db

import os



bp = Blueprint('blog', __name__)

# uploads_dir = os.path.join(bp.root_path, '/static/uploads')
# os.makedirs(uploads_dir, exist_ok=True)

def convertToBinaryData(filename):
    #Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title,description, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username , description, yturl'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)
    # print(post)
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        body = request.form['ckeditor']
        if request.files:
            titleimage = request.files['titleimage']
        yturl = request.form['yturl']

        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?, description = ? , yturl = ?'
                ' WHERE id = ?',
                (title, body, description,yturl, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/viewpost')
def viewpost(id):
    post = get_post(id)
    print(post)
    return render_template('blog/post.html',post=post)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    print(request.form)
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        body = request.form['ckeditor']
        titleimage = request.files['titleimage']
        yturl = request.form['yturl']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            cur=db.cursor()
            cur.execute(
                'INSERT INTO post (title, description, body, author_id,yturl)'
                ' VALUES (?, ?, ?, ?,?)',
                (title, description, body, g.user['id'],yturl)
            )
            db.commit()
            fname = str(cur.lastrowid)+"."+titleimage.filename.rsplit('.', 1)[1].lower()
            # titleimage.save(os.path.join(uploads_dir, fname))

            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')