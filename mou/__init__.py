from .route import (
    Mou,
    route,
    register_mou,
    before_request,
)
from .helper import (
    redirect,
    make_json,
)
from .template import MouTemplate
from .run import (
    run,
    request,
    make_response,
)

render_template = MouTemplate.render
register_filter = MouTemplate.register_filter
