from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='/home/joseph/Desktop/url_shortener/template')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
db = SQLAlchemy(app)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500))
    short_url = db.Column(db.String(10))

with app.app_context():
    db.create_all()

import random
import string

def generate_short_url():
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    while True:
        short_url = ''.join(random.choice(letters) for i in range(6))
        url = URL.query.filter_by(short_url=short_url).first()
        if not url:
            return short_url


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        original_url = request.form['url']
        url = URL.query.filter_by(original_url=original_url).first()
        if url:
            return redirect(url_for('display_short_url', short_url=url.short_url))
        else:
            short_url = generate_short_url()
            new_url = URL(original_url=original_url, short_url=short_url)
            db.session.add(new_url)
            db.session.commit()
            return redirect(url_for('display_short_url', short_url=short_url))
    return render_template('home.html')


@app.route('/<short_url>')
def display_short_url(short_url):
    url = URL.query.filter_by(short_url=short_url).first()
    if url:
        return render_template('short_url.html', original_url=url.original_url, short_url=url.short_url)
    else:
        return f'Short URL {short_url} not found'


@app.route('/<short_url>/redirect')
def redirect_to_original_url(short_url):
    url = URL.query.filter_by(short_url=short_url).first()
    if url:
        return redirect(url.original_url)
    else:
        return f'Short URL {short_url} not found'

if __name__ == '__main__':
    app.run(debug=True)

