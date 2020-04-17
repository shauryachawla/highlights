from app import app
from flask import render_template

@app.route('/')
@app.route('/sth')
def sth():
    user = {'username': "tyler", 'age':4}
    return render_template('index.html', title="shaurya ka blog", user=user)
