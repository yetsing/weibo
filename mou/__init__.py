from .mouse import (
    Mou,
    route,
    register_route,
)
from .helper import (
    redirect,
    make_json,
    MouTemplate,
    make_response,
)
from .run import run, request

render_template = MouTemplate.render
register_filter = MouTemplate.register_filter
