# coding=utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    search_content = StringField(validators=[DataRequired()])
    submit = SubmitField('Search')
