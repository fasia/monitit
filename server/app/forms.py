from flask_wtf import Form

from wtforms_alchemy import model_form_factory, ModelFieldList, ModelFormField
from wtforms import FormField, FieldList
from wtforms import StringField
from wtforms.validators import DataRequired

from app.server import db
from app.models import User, RecipeItem, Recipe, Category, Ingredient

BaseModelForm = model_form_factory(Form)

class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session

class UserCreateForm(ModelForm):
    class Meta:
        model = User

class SessionCreateForm(Form):
    email = StringField('name', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])

""" class UnitForm(ModelForm):
    class Meta:
        model = Unit """

class RecipeItemCreateForm(ModelForm):
    class Meta:
        model = RecipeItem
    #unit = ModelFormField(UnitForm)

class RecipeCreateForm(ModelForm):
    class Meta:
        model = Recipe
    #recipeitems = ModelFieldList(FormField(RecipeItemCreateForm))
    recipeitems = ModelFieldList(FormField(RecipeItemCreateForm))

    
#class LikeCreateForm(ModelForm):
#    class Meta:
#        model = Like

class RecipeUpdateForm(ModelForm):
    class Meta:
        model = Recipe

class RecipeItemUpdateForm(ModelForm):
    class Meta:
        model = RecipeItem

class ProfileUpdateForm(ModelForm):
    class Meta:
        model = User


# class EditProfileAdminForm(Form):
#     email = StringField('Email', validators=[Required(), Length(1, 64),Email()])
#   #  username = StringField('Username', validators=[Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames must have only letters, ''numbers, dots or underscores')])
#     def __init__(self, user, *args, **kwargs):
#         super(EditProfileAdminForm, self).__init__(*args, **kwargs)
#         self.role.choices = [(role.id, role.name)
#                         for role in Role.query.order_by(Role.name).all()]
#         self.user = user
#     def validate_email(self, field):
#         if field.data != self.user.email and User.query.filter_by(email=field.data).first():
#             raise ValidationError('Email already registered.')
#     def checkpass(self, field):
#         if field.data != self.user.password and User.query.filter_by(pa=field.data).first():
#             raise ValidationError('Username already in use.')
