
from wtforms import StringField, SubmitField , IntegerField, RadioField, FloatField , DateField ,BooleanField , ValidationError ,PasswordField, SelectField , TextAreaField
from wtforms.validators import DataRequired, Length, Email , NumberRange , Optional , EqualTo
from flask_wtf import FlaskForm
from api.db.driver import Driver
from flask_wtf.file import FileField, FileAllowed
import re

'''
How to use:
import classes from this file and use them in the main.py file
use flask to add the forms to the html file like this {{ object_name.object_attribute)placeholder ="Words in the box") }}.
if you have mulitple forms on 1 page use if form_name.submit_name.data and form_name.validate(): 
to check if the form is submitted and validated.Instead of the builtin method submit_and_validate()
'''


# ADDITIONAL CHECKS!
def password_check(form, field):
    password = field.data
    if not re.search(r'[A-Z]', password):
        raise ValidationError('Password must contain at least one uppercase letter')
    if not re.search(r'[a-z]', password):
        raise ValidationError('Password must contain at least one lowercase letter')
    if not re.search(r'\d', password):
        raise ValidationError('Password must contain at least one digit')
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError('Password must contain at least one special character')
    
def phone_check(form, field):
    phone = field.data
    if re.search(r'[a-zA-Z]', phone):
        raise ValidationError('Phone number must contain only numbers')
    if not re.search(r'[0-9]{8}', phone):
        raise ValidationError('Phone number must be 8 digits long')
    if not re.search(r'[0-9]{4}[0-9]{4}', phone):
        raise ValidationError('Phone number must be in the format XXXXXXXX')


# END OF ADDITIONAL CHECKS!


# USER FORMS
class UserCreationForm(FlaskForm):
    name_create = StringField('name', validators=[DataRequired(), Length(min=2, max=20)])
    name_last_create = StringField('name', validators=[DataRequired(), Length(min=2, max=20)])
    email_create = StringField('email', validators=[DataRequired(),Email()])
    password_create = PasswordField('password', validators=[DataRequired(),Length(min=8,max=20),password_check])
    password_confirm = PasswordField('repeat password', validators=[DataRequired(),EqualTo('password_create', message='Passwords must match')])
    address_create = StringField('address', validators=[DataRequired()])
    submit_user_create = SubmitField('Submit')


class UserGetbyIdForm(FlaskForm):
    id_get = StringField('id', validators=[DataRequired(), Length(min=36, max=36)])
    submit_user_get = SubmitField('Get User')


class UserDeletebyIdForm(FlaskForm):
    id_delete = StringField('id', validators=[DataRequired(), Length(min=36, max=36)])
    submit_user_delete = SubmitField('Submit')


class UserUpdateForm(FlaskForm):
    name_update = StringField('first name', validators=[Optional() ,Length(min=2, max=20)])
    name_last_update = StringField('last name', validators=[Optional() ,Length(min=2, max=20)])
    email_update = StringField('email', validators=[Optional() ,Email()])
    password_update = PasswordField('new password', validators=[Optional() ,Length(min=8,max=20),password_check])
    address_update = StringField('address', validators=[Optional()])
    old_password = PasswordField("old password",validators=[DataRequired()])
    password_confirm = PasswordField('confirm new password', validators=[EqualTo('password_update', message='Passwords must match')])
    submit_user_update = SubmitField('Submit')
    
class UserProfile(FlaskForm):
    image = FileField('Update Profile Picture', validators=[DataRequired(),FileAllowed(['png'], message="Only PNG files are allowed")])
    submit_profile = SubmitField('Update')


# USER SIGNIN FORM

class UserSignInForm(FlaskForm):
    email_signin = StringField('email', validators=[DataRequired(),Email()])
    password_signin = PasswordField('password', validators=[DataRequired(),Length(min=8,max=20)])
    remember_me = BooleanField('Remember me')
    submit_user_signin = SubmitField('Submit')


# PROMO FORMS
class PromoCreationForm(FlaskForm):
    promo_create = StringField('promo_ID', validators=[DataRequired(), Length(min=2, max=20)])
    type_create = RadioField('type', choices=[('value', 'Value'), ('percentage', 'Percentage')], default='percentage')
    value_create = IntegerField('discount', validators=[DataRequired(), NumberRange(min=0, max=100)])
    submit_promo_create = SubmitField('Submit')


class PromoGetbyIdForm(FlaskForm):
    promo_get = StringField('promo_ID', validators=[DataRequired(), Length(min=2, max=20)])
    submit_promo_get = SubmitField('Get Promo')


class PromoDeletebyIdForm(FlaskForm):
    promo_delete = StringField('promo_ID', validators=[DataRequired(), Length(min=2, max=20)])
    submit_promo_delete = SubmitField('Submit')


class PromoUpdateForm(FlaskForm):
    promo_update = StringField('promo_ID', validators=[DataRequired(), Length(min=0, max=20)])
    type_update = RadioField('type', choices=[('value', 'Value'), ('percentage', 'Percentage')], default='percentage')
    value_update = IntegerField('discount', validators=[Optional(), NumberRange(min=0, max=100)])
    submit_promo_update = SubmitField('Submit')


# PLAN FORMS
class PlanCreationForm(FlaskForm):
    # Maybe make this radio buttons
    plan_type_create = StringField('plan_type', validators=[DataRequired(), Length(min=2, max=20)])
    mean_cost_create = FloatField('mean_cost', validators=[DataRequired()])
    plan_description_create = StringField('description', validators=[DataRequired()])
    submit_plan_create = SubmitField('Submit')


class PlanGetbyTypeForm(FlaskForm):
    plan__type_get = StringField('plan_type', validators=[DataRequired(), Length(min=2, max=20)])
    submit_plan_get = SubmitField('Submit')


class PlanDeletebyTypeForm(FlaskForm):
    plan_type_delete = StringField('plan_type', validators=[DataRequired(), Length(min=2, max=20)])
    submit_plan_delete = SubmitField('Submit')


class PlanUpdateForm(FlaskForm):
    plan_type_update = StringField('plan_type', validators=[DataRequired(), Length(min=2, max=20)])
    mean_cost_update = FloatField('mean_cost', validators=[Optional()])
    plan_description_update = StringField('description', validators=[Optional(), Length(min=2, max=200)])
    submit_plan_update = SubmitField('Submit')


# BILL FORMS
class BillCreationForm(FlaskForm):
    bill_id_create = StringField('bill_id', validators=[DataRequired(), Length(min=2, max=20)])
    bill_status_create = RadioField('type', choices=[('True', 'Paid'), ('False', 'Unpaid')], default='False')
    bill_customer_id_create = StringField('bill_date', validators=[DataRequired()])
    submit_bill_create = SubmitField('Submit')


class BillGetbyIdForm(FlaskForm):
    bill_id_get = StringField('bill_id', validators=[DataRequired(), Length(min=2, max=20)])
    submit_bill_get = SubmitField('Submit')


class BillDeletebyIdForm(FlaskForm):
    bill_id_delete = StringField('bill_id', validators=[DataRequired(), Length(min=2, max=20)])
    submit_bill_delete = SubmitField('Submit')


class BillUpdateForm(FlaskForm):
    bill_id_update = StringField('bill_id', validators=[DataRequired(), Length(min=2, max=20)])
    bill_status_update = RadioField('type', choices=[('True', 'Paid'), ('False', 'Unpaid')], default='False')
    bill_customer_id_update = StringField('bill_date', validators=[Optional()])
    submit_bill_update = SubmitField('Submit')


# ITEM FORMS
class ItemCreationForm(FlaskForm):
    item_id_create = StringField('item_id', validators=[DataRequired(), Length(min=36, max=36)])
    owner_id_create = StringField('owner_id', validators=[DataRequired(), Length(min=36, max=36)])
    item_status_description_create = StringField('item_price', validators=[DataRequired(), Length(min=2, max=200)])
    item_status_date_create = DateField('item_description', validators=[DataRequired()])
    item_past_repair_status_description_create = StringField('past_repair',
                                                             validators=[DataRequired(), Length(min=2, max=200)])
    item_past_repair_status_start_date_create = DateField('past_repair_date', validators=[DataRequired()])
    item_past_repair_status_end_date_create = DateField('past_repair_end_date', validators=[DataRequired()])
    item_current_repair_status_description_create = StringField('current_repair',
                                                                validators=[DataRequired(), Length(min=2, max=200)])
    item_current_repair_status_start_date_create = DateField('current_repair_date', validators=[DataRequired()])
    item_current_repair_status_end_date_create = DateField('current_repair_end_date', validators=[DataRequired()])
    item_address_create = StringField('item_address', validators=[DataRequired(), Length(min=2, max=200)])
    item_subscription_create = StringField('plan_type', validators=[DataRequired(), Length(min=2, max=200)])
    item_subscription_start_date_create = DateField('subscription_start_date', validators=[DataRequired()])
    item_subscription_end_date_create = DateField('subscription_end_date', validators=[DataRequired()])
    submit_item_create = SubmitField('Submit')


class ItemGetbyIdForm(FlaskForm):
    item_get_by = RadioField('type', choices=[('item_id', 'Item_id'), ('owner_id', 'owner_id')], default='item_id')
    item_id_get = StringField('id', validators=[DataRequired(), Length(min=36, max=36)])
    submit_item_get = SubmitField('Submit')


class ItemDeletebyIdForm(FlaskForm):
    item_delete_by = RadioField('type', choices=[('item_id', 'Item_id'), ('owner_id', 'owner_id')], default='item_id')
    item_id_delete = StringField('id', validators=[DataRequired(), Length(min=36, max=36)])
    submit_item_delete = SubmitField('Submit')


class ItemUpdateForm(FlaskForm):
    item_update_by = RadioField('type', choices=[('item_id', 'Item_id'), ('owner_id', 'owner_id')], default='item_id')
    item_id_update = StringField('item_id', validators=[Optional(), Length(min=36, max=36)])
    owner_id_update = StringField('owner_id', validators=[Optional(), Length(min=36, max=36)])
    item_status_description_update = StringField('item_price', validators=[Optional(), Length(min=2, max=200)])
    item_status_date_update = DateField('item_description', validators=[Optional(), DataRequired()])
    item_past_repair_status_description_update = StringField('past_repair',
                                                             validators=[Optional(), Length(min=2, max=200)])
    item_past_repair_status_start_date_update = DateField('past_repair_date', validators=[Optional(), DataRequired()])
    item_past_repair_status_end_date_update = DateField('past_repair_end_date', validators=[Optional(), DataRequired()])
    item_current_repair_status_description_update = StringField('current_repair',
                                                                validators=[Optional(), Length(min=2, max=200)])
    item_current_repair_status_start_date_update = DateField('current_repair_date',
                                                             validators=[Optional(), DataRequired()])
    item_current_repair_status_end_date_update = DateField('current_repair_end_date',
                                                           validators=[Optional(), DataRequired()])
    item_address_update = StringField('item_address', validators=[Optional(), Length(min=2, max=200)])
    item_subscription_update = StringField('plan_type', validators=[Optional(), Length(min=2, max=200)])
    item_subscription_start_date_update = DateField('subscription_start_date', validators=[Optional()])
    item_subscription_end_date_update = DateField('subscription_end_date', validators=[Optional()])
    submit_item_update = SubmitField('Submit')


# INSURANCE FORMS

class InsuranceForm(FlaskForm):
    user_age = IntegerField('age', validators=[DataRequired(), NumberRange(min=18, max=100)])
    user_gender = RadioField('gender', choices=[('Female', 'Female'), ('Male', 'Male')], validators=[DataRequired()])
    user_job = SelectField('job',
                           choices=[('1', 'Student'), ('0', 'Blue Collar'), ('1', 'White Collar'), ('1', 'Unemployed')],
                           validators=[DataRequired()])
    user_sports = RadioField('user_sports', choices=[('1', 'Yes'), ('0', 'No')], validators=[DataRequired()])
    user_education = SelectField('user_edu', choices=[('Associate degree', 'Associate degree'),
                                                      ('High school diploma or equivalent',
                                                       'High school diploma or equivalent'),
                                                      ('Some college, no degree', 'In college, no degree'),
                                                      ('Less than high school', 'Less than high school'),
                                                      ('Bachelor’s degree', 'Bachelor’s degree'),
                                                      ('Doctoral degree', 'Doctoral degree'),
                                                      ('Master’s degree', 'Master’s degree')],
                                 validators=[DataRequired()])
    user_vacations = IntegerField('vacations', validators=[DataRequired(), NumberRange(min=0, max=100)])
    user_phone_price = IntegerField('phoneprice', validators=[DataRequired(), NumberRange(min=0, max=10000)])
    user_plan = SelectField('plan', choices=[('1', 'Bronze'), ('2', 'Silver'), ('3', 'Gold')],
                            validators=[DataRequired()])
    submit_insure = SubmitField('Submit')
    
# CONTACT US 

class ContactUs(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(),Email()])
    phone_number = StringField('phone number', validators=[DataRequired(),phone_check])
    message = TextAreaField('message', validators=[DataRequired()])
    submit_contact = SubmitField('Submit')
    
#SEARCH

class SearchForm(FlaskForm):
    search = StringField('search', validators=[DataRequired()])
    submit_search = SubmitField('')