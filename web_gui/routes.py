from flask import render_template, redirect, url_for, flash, make_response, session, request
from web_gui import site
from classes.class_database import DataBase
from web_gui.forms import LogFeeding, Login, RegisterUser
from datetime import datetime
from fpdf import FPDF, HTMLMixin
from pytz import timezone


class HTML2PDF(FPDF, HTMLMixin):
    pass


@site.route('/login', methods=['GET', 'POST'])
def login():
    db = DataBase()
    username = request.form['username']
    password = request.form['password']

    result = db.validate(username=username, password=password)
    print(result)
    if result is True:
        session['logged_in'] = True
        session['user'] = request.form['username']

    else:
        flash('Wrong Username or Password')

    return redirect('/')


@site.route("/logout")
def logout():
    session['logged_in'] = False
    flash('{} has been successfully logged out'.format(session['user']))
    return redirect('/')


@site.route('/pdf', methods=['GET'])
def jpg_to_pdf():
    if not session.get('logged_in'):
        form = Login()
        return render_template('login.html', form=form)
    else:
        pdf = HTML2PDF(orientation='L')
        db = DataBase()
        results = db.get_all_records()
        html = render_template('generate_pdf.html', results=results)

        pdf.add_page()
        pdf.write_html(html)

        response = make_response(pdf.output(dest='S').encode('latin-1'))
        response.headers.set('Content-Disposition', 'attachment', filename='bens_feeding_report.pdf')
        response.headers.set('Content-Type', 'application/pdf')

        return response


@site.route('/', methods=['GET'])
@site.route('/feeding_report', methods=['GET', 'POST'])
def event_report():
    if not session.get('logged_in'):
        form = Login()
        return render_template('login.html', form=form)
    else:
        db = DataBase()
        results = db.get_all_records()

        db.close_connections()

    return render_template('bens_tracker.html', results=results)


@site.route('/log_event', methods=['GET', 'POST'])
def log_event():
    if not session.get('logged_in'):
        form = Login()
        return render_template('login.html', form=form)
    else:
        db = DataBase()
        form = LogFeeding()
        test = timezone('US/Eastern')

        if form.validate_on_submit() is True:
            eastern = timezone('US/Eastern')
            date = datetime.now(eastern).strftime('%Y-%m-%d')

            time = form.time.data
            event_type = form.type.data
            notes = form.note.data

            if event_type == 'start_feed':
                db.new_entry(start_feed=time, date=date, notes=notes)
                flash('Event Logged')
                db.close_connections()
                return redirect(url_for('event_report'))
            if event_type == 'end_feed':
                prev_record = db.get_last_record(date=date)
                prev_record_id = prev_record[0]['id']

                db.new_entry(end_feed=time, id=prev_record_id, notes=notes)
                flash('Event Logged')
                db.close_connections()
                return redirect(url_for('event_report'))
            if event_type == 'bottle':
                db.new_entry(bottle=time, date=date, notes=notes)
                flash('Event Logged')
                db.close_connections()
                return redirect(url_for('event_report'))
            if event_type == 'poop_time':
                db.new_entry(poop_time=time, date=date, notes=notes)
                flash('Event Logged')
                db.close_connections()
                return redirect(url_for('event_report'))
            if event_type == 'pee_time':
                db.new_entry(pee_time=time, date=date, notes=notes)
                flash('Event Logged')
                db.close_connections()
                return redirect(url_for('event_report'))
            if event_type == 'both':
                db.new_entry(both=time, date=date, notes=notes)
                flash('Event Logged')
                db.close_connections()
                return redirect(url_for('event_report'))

    return render_template('/log_event.html', form=form)


@site.route('/register', methods=['GET', 'POST'])
def register():
    if not session.get('logged_in'):
        form = Login()
        return render_template('login.html', form=form)
    elif session['user'] != 'admin':
        flash('You are not authorized to view this page.')
        return redirect('/not_auth')
    else:
        form = RegisterUser()
        if form.validate_on_submit():
            db = DataBase()
            username = form.username.data
            password = form.password.data
            result = db.add_user(username=username, password=password)
            if result == 'Success':
                flash('New user has been successfully added.')
                return redirect('/')

        return render_template('register_user.html', form=form)


@site.route('/not_auth', methods=['GET'])
def not_auth():
    if not session.get('logged_in'):
        form = Login()
        return render_template('login.html', form=form)
    else:
        return render_template('not_auth.html')
