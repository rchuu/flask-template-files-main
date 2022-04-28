from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.show import Show


@app.route('/add/show')
def add_show():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    return render_template('add_show.html', user=User.get_from_id(data))


@app.route('/create/show', methods=['POST'])
def create_show():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Show.validate_show(request.form):
        return redirect('/add/show')
    data = {
        "title": request.form["title"],
        "network": request.form["network"],
        "description": request.form["description"],
        "release_date": request.form["release_date"],
        "user_id": session['user_id']
    }
    Show.save(data)
    return redirect('/success')


@app.route('/edit/show/<int:id>')
def edit_show(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    user_data = {
        "id": session['user_id']
    }
    return render_template("edit_show.html", edit=Show.get_one(data), user=User.get_from_id(user_data))


@app.route('/update/show', methods=['POST'])
def update_show():
    print(request.form)
    if 'user_id' not in session:
        return redirect('/logout')
    if not Show.validate_show(request.form):
        return redirect('/add/show')
    data = {
        "title": request.form["title"],
        "network": request.form["network"],
        "description": request.form["description"],
        "release_date": request.form["release_date"],
        "id": request.form['id']
    }
    Show.update(data)
    return redirect('/success')


@app.route('/show/<int:id>')
def view_show(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    user_data = {
        "id": session['user_id']
    }
    return render_template("view_show.html", show=Show.get_one(data), shows=Show.get_user_shows(data), user=User.get_from_id(user_data))


@app.route('/destroy/show/<int:id>')
def destroy_show(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    Show.destroy(data)
    return redirect('/success')


@app.route('/like/show<int:id>')
def like_show(id):
    if 'user_id' not in session:
        return redirect('/logout')

    if "count" not in session:
        session["count"] = 0
    else:
        session['count'] += 1
    data = {
        "id": id
    }
    user_data = {
        "id": session['user_id']
    }
    return render_template("view_show.html", user_likes=Show.get_user_likes(user_data), shows_like=Show.get_user_shows(data), user=User.get_likes_users(user_data))
