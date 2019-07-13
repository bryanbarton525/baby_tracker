from flask import render_template, redirect, url_for, flash
from web_gui import site
from classes.class_database import DataBase
from web_gui.forms import LogFeeding
from datetime import datetime


@site.route('/feeding_report', methods=['GET', 'POST'])
def event_report():
    db = DataBase()
    results = db.get_all_records()
    print(results)

    return render_template('bens_tracker.html', results=results)


@site.route('/', methods=['GET', 'POST'])
@site.route('/log_event', methods=['GET', 'POST'])
def log_event():
    db = DataBase()
    form = LogFeeding()

    if form.validate_on_submit() is True:
        date = datetime.today().strftime('%Y-%m-%d')
        print("submitted")
        time = form.time.data
        event_type = form.type.data
        notes = form.note.data
        print(time)
        print(event_type)
        if event_type == 'start_feed':
            print(date)
            db.new_entry(start_feed=time, date=date, notes=notes)
            flash('Event Logged')
            return redirect(url_for('event_report'))
        if event_type == 'end_feed':
            prev_record = db.get_last_record()
            prev_record_id = prev_record[0]['id']
            print(prev_record_id)
            db.new_entry(end_feed=time, id=prev_record_id, notes=notes)
            flash('Event Logged')
            return redirect(url_for('event_report'))
        if event_type == 'bottle':
            db.new_entry(bottle=time, date=date, notes=notes)
            flash('Event Logged')
            return redirect(url_for('event_report'))
        if event_type == 'poop_time':
            db.new_entry(poop_time=time, date=date, notes=notes)
            flash('Event Logged')
            return redirect(url_for('event_report'))
        if event_type == 'pee_time':
            db.new_entry(pee_time=time, date=date, notes=notes)
            flash('Event Logged')
            return redirect(url_for('event_report'))

    return render_template('/log_event.html', form=form)
