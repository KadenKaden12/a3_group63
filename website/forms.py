from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, DateTimeField, TimeField, IntegerField, SelectField, DateTimeLocalField
from wtforms.validators import InputRequired, Length, Email, EqualTo, DataRequired, NumberRange
from flask_login import current_user

# creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    user_name = StringField('Username', validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=150)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=150)])
    sur_name = StringField('Surname', validators=[DataRequired(), Length(max=150)])
    contact_no = StringField('Contact Number', validators=[DataRequired(), Length(max=150)])
    stress_address = StringField('Street Address', validators=[DataRequired(), Length(max=200)])
    submit = SubmitField('Register')
    # user_name=StringField("User Name", validators=[InputRequired()])
    # email = StringField("Email Address", validators=[Email("Please enter a valid email")])
    # # linking two fields - password should be equal to data entered in confirm
    # password=PasswordField("Password", validators=[InputRequired(),
    #               EqualTo('confirm', message="Passwords should match")])
    # confirm = PasswordField("Confirm Password")

    # # submit button
    # submit = SubmitField("Register")

class EventRegisterForm(FlaskForm):
    user = current_user
    event_name = StringField('Event Name', validators=[DataRequired(), Length(max=300)])
    location = StringField('Location', validators=[DataRequired(), Length(max=150)])
    event_date = DateTimeLocalField('Event Date', validators=[DataRequired()], render_kw={"type": "datetime-local"})
    start_from = TimeField('Start Time', validators=[DataRequired()])
    end_to = TimeField('End Time', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=300)])
    image_path = StringField('Image Path', validators=[DataRequired(), Length(max=500)])
    no_of_tickets = IntegerField('Number of Tickets', validators=[DataRequired(), NumberRange(min=1)])

    # category_id = IntegerField('Category ID', validators=[DataRequired()])
    # status_id = IntegerField('Status ID', validators=[DataRequired()])
    owner_id = IntegerField('', default=user.id if user and user.is_authenticated else 0, render_kw={"type": "hidden"})
    category_id = SelectField('Category', coerce=int)
    status_id = SelectField('Status', coerce=int)

    submit = SubmitField('Register Event')
    
class EventUpdateForm(FlaskForm):
    event_name = StringField('Event Name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    event_date = DateTimeField('Event Date', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    start_from = StringField('Start Time', validators=[DataRequired()])
    end_to = StringField('End Time', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    image_path = StringField('Image Path')
    no_of_tickets = IntegerField('No of Tickets', validators=[DataRequired()])
    category_id = SelectField('Category', coerce=int)
    submit = SubmitField('Update Event')

class OrderForm(FlaskForm):
    no_of_tickets = IntegerField('Number of Tickets', validators=[DataRequired(), NumberRange(min=1, message="Must be at least 1 ticket")])