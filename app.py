from flask import Flask, request, flash, url_for, redirect, render_template

from flask_sqlalchemy import SQLAlchemy

from songs import *

from flask_login import UserMixin, LoginManager, login_user, login_required, current_user

from werkzeug.security import generate_password_hash, check_password_hash
import numpy as np

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'

db = SQLAlchemy(app)

class user(UserMixin, db.Model):
   id = db.Column('user_id', db.Integer, primary_key = True)
   username = db.Column(db.String(100), unique=True)
   password = db.Column(db.String(100))
   center1 = db.Column(db.String(700))
   center2 = db.Column(db.String(700))

   def __init__(self, username, password, center1, center2):
       self.username = username
       self.password = password
       self.center1 = center1
       self.center2 = center2


@app.route('/', methods = ['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        
        username = request.form['username']
        password = request.form['password']

        is_user = user.query.filter_by(username=username).first()

        print(username)
        print(password)

        if is_user:
            if check_password_hash(is_user.password, password):
                return redirect(url_for('results'))
            else:
                return redirect(url_for('login'))

        new_user = user(username=username, password=generate_password_hash(password, method='sha256'), center1="", center2="")

        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('poll'))

    return render_template("login.html")



@app.route('/poll', methods = ['GET', 'POST'])
@login_required


def poll():
    progress_val = 0
    yes_num = 0
    no_num = 0

    store_ids_yes = []

    store_ids_no = []
    song_id, preview_url, image_url = get_rand_song()
    
    data = [song_id, preview_url, image_url, progress_val]

    if request.method == 'POST':
        
        if request.form['submit_button'] == 'YES':
            if yes_num < 5:
                yes_num += 1
                progress_val += 10
                store_ids_yes.append(song_id)
        elif request.form['submit_button'] == 'NO':
            if no_num < 5:
                no_num += 1
                progress_val += 10
                store_ids_no.append(song_id)
        data = [song_id, preview_url, image_url, progress_val]
        
        if yes_num >= 5 and no_num >= 5:
            current_user.center1 = str(calculate_center(store_ids_yes));
            current_user.center2 = str(calculate_center(store_ids_no));
            db.session.commit()
            return redirect(url_for("results"))
        else:
            return render_template("poll.html", data=data)

    return render_template("poll.html", data=data)
    


@app.route('/results')
@login_required
def results():
    
    data = get_friends_list(current_user.center1, current_user.center2)

    return render_template('results_page.html', data=data)


def get_friends_list(center1, center2):

    all_data = user.query.all()

    dist1 = []
    dist2 = []

    center1 = np.fromstring(center1[1:-1], dtype=np.float, sep=' ')
    center2 = np.fromstring(center2[1:-1], dtype=np.float, sep=' ')
    
    for user in all_data:
        
        u_cent1 = user.center1
        u_cent2 = user.center2

        u_cent1 = np.fromstring(u_cent1[1:-1], dtype=np.float, sep=' ')
        u_cent2 = np.fromstring(u_cent2[1:-1], dtype=np.float, sep=' ')
        
        dist1.append((user.username, np.linalg.norm(center1 - u_cent1)))
        dist2.append((user.username, np.linalg.norm(center2 - u_cent2)))

    dist1.sort(key=lambda i:i[1], reverse=True)
    dist2.sort(key=lambda i:i[1], reverse=True)
    
    return (dist1, dist2)

if __name__ == '__main__':
    db.create_all()

    app.secret_key = 'akskfjoadjfjaofjs'
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(userid):
       return user.query.get(int(userid))

    app.run()
