from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from startup_setup import Base, Startup, Founder

app = Flask(__name__)

engine = create_engine('sqlite:///startup.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# list startups


@app.route('/')
@app.route('/startups')
def list_startups():
    startups = session.query(Startup).all()
    return render_template('startups.html', startups=startups)


# show startup
@app.route('/startups/<int:startup_id>')
def show_startup(startup_id):
    startup = session.query(Startup).filter_by(id=startup_id).one()
    founders = session.query(Founder).filter_by(startup_id=startup.id).all()
    return render_template('show_startup.html', startup=startup, founders=founders)


# add founder
@app.route('/startups/<int:startup_id>/new', methods=['GET', 'POST'])
def new_founder(startup_id):
    if request.method == 'POST':
        new_founder = Founder(
            name=request.form['name'], bio=request.form['bio'], startup_id=startup_id)
        startup_id = startup_id
        session.add(new_founder)
        session.commit()
        return redirect(url_for('startupMenu', startup_id=startup_id))
    else:
        return render_template('newmenuitem.html', startup_id=startup_id)


# edit founder
@app.route('/startups/<int:founder_id>/edit', methods=['GET', 'POST'])
def edit_founder(founder_id):
    edited_founder = session.query(Founder).filter_by(id=founder_id).one()
    if request.method == 'POST':
        if request.form['name']:
            edited_founder.name = request.form['name']
        if request.form['bio']:
            edited_founder.bio = request.form['bio']
        session.add(edited_founder)
        session.commit()
        return redirect(url_for('show_startup', founder=edited_founder, startup_id=edited_founder.startup_id))
    else:
        return render_template(
            'edit_founder.html', founder=edited_founder)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
