from wtforms import StringField, SubmitField , IntegerField
from wtforms.validators import DataRequired, Length, Email , NumberRange
from flask_wtf import FlaskForm

class UserForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(min=2, max=20)], description="name")
    email = StringField('email', validators=[DataRequired(),Email()])
    password = StringField('password', validators=[DataRequired(),Length(min=8,max=20)])
    age = IntegerField('age',  validators=[DataRequired(),NumberRange(min=18, max=100)])
    address = StringField('address', validators=[DataRequired()])
    submit = SubmitField('CreateUser')