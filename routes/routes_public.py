from mou import render_template, Mou
from routes import current_user

default = Mou('index')


@default.route('/')
def index():
    u = current_user()
    return render_template('index.html', username=u.username)
