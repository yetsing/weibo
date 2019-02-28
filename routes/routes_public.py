from mou import (
    Mou,
    request,
    render_template,
)

default = Mou('index')


@default.route('/')
def index():
    u = request.current_user
    return render_template('index.html', username=u.username)
