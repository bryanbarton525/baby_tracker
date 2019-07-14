from flask import render_template, redirect, url_for, flash, make_response
from web_gui import site
from classes.class_database import DataBase
from web_gui.forms import LogFeeding
from datetime import datetime
from fpdf import FPDF, HTMLMixin


class HTML2PDF(FPDF, HTMLMixin):
    pass


@site.route('/pdf', methods=['GET'])
def jpg_to_pdf():
    pdf = HTML2PDF(orientation='L')
    db = DataBase()
    results = db.get_all_records()
    html = render_template('generate_pdf.html', results=results)
    print(html)
    pdf.add_page()
    pdf.write_html(html)

    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers.set('Content-Disposition', 'attachment', filename='bens_feeding_report.pdf')
    response.headers.set('Content-Type', 'application/pdf')

    return response


@site.route('/feeding_report', methods=['GET', 'POST'])
def event_report():
    db = DataBase()
    results = db.get_all_records()
    print(results)
    db.close_connections()

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
            db.close_connections()
            return redirect(url_for('event_report'))
        if event_type == 'end_feed':
            prev_record = db.get_last_record()
            prev_record_id = prev_record[0]['id']
            print(prev_record_id)
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

    return render_template('/log_event.html', form=form)
