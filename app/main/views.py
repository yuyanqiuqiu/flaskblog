# -*- coding: utf-8 -*- 
from datetime import datetime
from flask import render_template, session, request, abort, redirect, url_for
from flask_login import login_required

from . import main  # 同级的用.
from .forms import NameForm
from .. import db
from ..models import User


@main.route('/',methods=['GET','POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        user = User.query.filter_by(username=name).first()
        if user is None:
            user = User(username=name)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            # send_email('test@example.com','New User','new_user',new_user_name=name)
        else:
            session['known'] = True
        session['name'] = name
        form.name.data = ''
        return redirect(url_for('.index'))
    return render_template('name.html', form=form, name=session.get('name'), \
                           known=session.get('known'))


@main.route('/secret',methods=['GET','POST'])
@login_required
def secret():
    return '只有登陆用户才可以看到内容'