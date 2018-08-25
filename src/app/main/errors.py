# coding=utf-8
from . import main
from flask import render_template
from .forms import SearchForm


@main.app_errorhandler(404)
def page_not_found(e):
    form = SearchForm()
    return render_template('404.html',form=form), 404
