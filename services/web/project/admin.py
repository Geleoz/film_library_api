"""
Initializes and configures flask admin and his views
"""
from flask_login import current_user
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from project import app, db
from project.models import Role, User, Genre, Director, Film


class CustomModelView(ModelView):
    """
    Customized model view
    """
    def is_accessible(self):
        """
        Checks if user has access to this view
        :return: bool
        """
        return current_user.is_authenticated and current_user.is_admin()


class CustomAdminIndexView(AdminIndexView):
    """
    Customized admin index view
    """
    def is_accessible(self):
        """
        Checks if user has access to this view
        :return: bool
        """
        return current_user.is_authenticated and current_user.is_admin()


admin = Admin(app, index_view=CustomAdminIndexView(), template_mode="bootstrap4")
admin.add_view(CustomModelView(Film, db.session))
admin.add_view(CustomModelView(Director, db.session))
admin.add_view(CustomModelView(Genre, db.session))
admin.add_view(CustomModelView(User, db.session))
admin.add_view(CustomModelView(Role, db.session))
