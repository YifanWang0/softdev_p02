from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length, EqualTo
from wtforms import widgets

# sign up form
class SignUpForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(),
                                       Length(min=4, max=80)])
    password = PasswordField(
        'Password', validators=[DataRequired(),
                                Length(min=6, max=80)])
    password_repeat = PasswordField('Password',
                                    validators=[
                                        DataRequired(),
                                        Length(min=6, max=80),
                                        EqualTo('password')
                                    ])
    submit = SubmitField('Sign Up')


# log in form
class LogInForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(),
                                       Length(min=4, max=80)])
    password = PasswordField(
        'Password', validators=[DataRequired(),
                                Length(min=6, max=80)])
    submit = SubmitField('Log In')
    
class SearchForm(FlaskForm):
    rarities = MultiCheckboxField('Filter by rarity:', choices=RARITY_OPTIONS)
    types = MultiCheckboxField('Filter by type:', choices=TYPE_OPTIONS)
    search = StringField('Query:', validators=[Length(min=0, max=80)])
    submit = SubmitField('Search')
