from flask import render_template

from . import main

__author__ = 'Xomak'


@main.route('/', methods=['GET', 'POST'])
def main():
    return render_template('main.html')
