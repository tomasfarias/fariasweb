from flask_wtf import FlaskForm
from flask_pagedown.fields import PageDownField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField, FieldList, Field, IntegerField, FormField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class NoValidateSelectMultipleField(SelectMultipleField):

    def pre_validate(self, form):
        pass


class CreateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = PageDownField('Body', validators=[DataRequired()])
    tags = NoValidateSelectMultipleField('Tags')
    submit = SubmitField('Publish')
