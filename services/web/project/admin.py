from project import app, db
from project.models import Role, User, Genre, Director, Film
from flask import abort
from flask_login import current_user
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView


class CustomModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()

    def inaccessible_callback(self, name, **kwargs):
        return abort(403)


class CustomAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()

    def inaccessible_callback(self, name, **kwargs):
        return abort(403)


admin = Admin(app, index_view=CustomAdminIndexView(), template_mode="bootstrap4")
admin.add_view(CustomModelView(Film, db.session))
admin.add_view(CustomModelView(Director, db.session))
admin.add_view(CustomModelView(Genre, db.session))
admin.add_view(CustomModelView(User, db.session))
admin.add_view(CustomModelView(Role, db.session))
