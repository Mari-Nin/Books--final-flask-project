from flask import url_for
from markupsafe import Markup
from flask_admin.form import ImageUploadField
from os import path
from src.config import Config
from wtforms.fields import SelectField
from src.admin_views.base import SecureModelView
from src.admin_views.utils import generate_name



class Bookview(SecureModelView):
    can_delete=True
    can_create=True
    can_edit=True

    edit_modal=True
    create_modal=True

    form_overrides = {
        'img': ImageUploadField,
    }

    form_args = {
        'img': {
            'base_path': path.join(path.dirname(Config.UPLOAD_PATH), '../'),
            'relative_path': 'static/uploads'
        }
    }


    column_formatters = {
    'img': lambda v, c, m, n: Markup(f'<img src="/{m.img}" width="70">') 
            }
    column_editable_list = ['img','location','title','quantity','status','category']
    column_filters = ['location','title','quantity','status','category']
    column_searchable_list = ['location','title','quantity','status','category']
    column_list = ['location','title','quantity','status','category']

    can_view_details=True
    details_modal=True

    can_export = True
  
  
    
