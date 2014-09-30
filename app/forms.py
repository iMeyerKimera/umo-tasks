# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import TextField, DateField, IntegerField, \
SelectField
from wtforms.validators import DataRequired

"""
We’re now going to use a powerful Flask extension called WTForms to help with form han-
dling and data validation. Remember how we need to create the AddTaskForm() form? Let’s
do that now.

First, install the package.

pip install Flask-WTF==0.9.4

"""

class AddTaskForm(Form):
    task_id = IntegerField('Priority')
    name = TextField('Task Name', validators=[DataRequired()])
    due_date = DateField('Date Due (mm/dd/yyyy)',
                         validators=[DataRequired()], format='%m/%d/%Y')

    priority = SelectField('Priority', validators=[DataRequired()],
                           choices=[('1', '1'), ('2', '2'), ('3', '3'),
                                    ('4', '4'), ('5', '5'),
                                    ('6', '6'), ('7', '7'), ('8', '8'),
                                    ('9', '9'), ('10', '10')])
status = IntegerField('Status')

"""
Notice how we’re importing from both Flask-WTF and WTForms . Essentially, Flask-WTF
works in tandem with WTForms, abstracting some of the functionality.
Save the form in the root directory.
"""
