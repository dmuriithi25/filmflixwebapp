import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

#READING EACH ROW IN (filmFlix.db)
def get_db_connection():        #opens connection to the filmFlix Db file
    conn = sqlite3.connect('filmFlix.db')
    conn.row_factory = sqlite3.Row  #name based access to each column in Db. Returns rows that look like python dictionaries
    return conn     #returns conn object used to access the Db

#ID: FETCHING FILM IDs TO LINK URL ON INDEX.HTML TO EACH FILM (identity.html)
#copy this to DELETE by film name
def get_film(filmID):
   conn = get_db_connection()
   film = conn.execute('SELECT * FROM tblFilms WHERE filmID = ?',
                       (filmID,)).fetchone()
   conn.close()
   if film is None:
      abort(404)
   return film
   

app = Flask(__name__)

#SECRET KEY
app.config['SECRET_KEY'] = 'top secret key'


# CREATE: HANDLING NEW FORM SUBMISSION (create.html) AND flash() MESSAGE FOR EMPTY FIELDS
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        yearReleased = request.form['yearReleased']
        rating = request.form['rating']
        duration = request.form['duration']
        genre = request.form['genre']

        if not title:
            flash('Not too fast! Please enter the Film Title!')
        elif not yearReleased:
            flash('Not too fast! Please enter the Release Year!')
        elif not rating:
            flash('Not too fast! Please enter the Film Rating!')
        elif not duration:
            flash('Not too fast! Please enter the Film Duration in mins!')
        elif not genre:
            flash('Not too fast! Please enter the Film Genre!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO tblFilms (title, yearReleased, rating, duration, genre) VALUES (?, ?, ?, ?, ?)',
                   (title, yearReleased, rating, duration, genre))
            
            conn.commit()
            conn.close()

            return redirect(url_for('index'))

    return render_template('create.html')


#INDEX: FETCHING ALL FILMS TO DISPLAY ON THE LANDING PAGE (index.html)
@app.route('/')
def index():
    conn = get_db_connection()
    tblFilms = conn.execute('SELECT * FROM tblFilms').fetchall()    #SQL query to select all entries in the table. Fetchall() fetch all rows (returns a list of films inserted into the db, init.db file)

    conn.close()    #close the connection
    return render_template('index.html', tblFilms=tblFilms)     #return the results of HTML file rendering & pass filmFlix as an arguement. Allows me to access the films in the index.html file


#ID: LINKING THE FILM IDs COLLECTED TO THE INDIVIDUAL FILMS IN (identity.html)
@app.route('/<int:filmID>')
def identity(filmID):
    film = get_film(filmID)
    return render_template('identity.html', film=film)


#EDIT: HANDLING EDIT SUBMISSIONS AND flash() MESSAGE FOR EMPTY FIELDS
@app.route('/<int:filmID>/edit', methods=('GET', 'POST'))
def edit(filmID):
    film = get_film(filmID)

    if request.method == 'POST':
        title = request.form['title']
        yearReleased = request.form['yearReleased']
        rating = request.form['rating']
        duration = request.form['duration']
        genre = request.form['genre']

        if not title:
            flash('Not too fast! Please enter the Film Title!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE tblFilms SET title = ?, yearReleased = ?, rating = ?, duration = ?, genre = ?' 'WHERE filmID = ?',
                   (title, yearReleased, rating, duration, genre, filmID))
            
            conn.commit()
            conn.close()

            return redirect(url_for('index'))
        
    return render_template('edit.html', film=film, filmID=filmID)

#DELETE: DELETING FILES AND flask() IF SUCCESSFULLY DELETED
#Switch to delete by film name instead of id
@app.route('/<int:filmID>/delete', methods=('POST',))
def delete(filmID):
    delete = get_film(filmID)
    conn = get_db_connection()
    conn.execute('DELETE FROM tblFilms WHERE filmID = ?', (filmID,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(delete['title']))

    return redirect(url_for('index'))