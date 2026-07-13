from wtforms.fields import SelectField
from src.admin_views.base import SecureModelView

class UserView(SecureModelView):
    can_delete=True
    can_create=True
    can_edit=True

    edit_modal=True
    create_modal=True
    form_overrides = {
        "role": SelectField
    }

    form_args = {
        'role': {'choices':['admin','user']}

    }
