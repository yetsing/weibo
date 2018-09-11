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
from .utils import log
from .run import run, request

render_template = MouTemplate.render
