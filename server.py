import json
from flask import Flask, render_template, request, redirect, flash, url_for
#import pdb
#import logging

# pdb.set_trace()
# à utiliser en lieu et place de import pdb et pdb.set_trace() :
# breakpoint()

# logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(filename='events.log', encoding='utf-8', level=logging.DEBUG)
# pour que chaque exécution reprenne un fichier vierge :
# logging.basicConfig(filename='example.log', filemode='w', level=logging.DEBUG)
# logging.debug("Informations détaillées sur le déroulement du programme")


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary', methods=['POST'])
def showSummary():
    list_valid_email = [club['email'] for club in clubs]
    error = None
    # ajout de la vérification de l'email
    if request.form['email'] not in list_valid_email:
        error = "This email is not valid."
        return render_template('index.html', error=error)
    else:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    club_name = club['name']
    # ajout dans le doctionnaire competition de la clé club_name correspondant au nb de places déjà réservées
    competition.setdefault(club_name, 0)
    print("places réservées avant:", competition[club_name])
    placesRequired = int(request.form['places'])
    places_after_booking = int(competition['numberOfPlaces'])-placesRequired
    points_after_booking = int(club["points"])-placesRequired
    # ajout d'un if/else et maj des points
    if places_after_booking >= 0 and competition[club_name] < 12 and placesRequired <= 12:
        competition['numberOfPlaces'] = places_after_booking
        club["points"] = points_after_booking
        competition[club_name] += placesRequired
        print("places réservées après :", competition[club_name])
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions)
    else: 
        flash('Vous ne pouvez pas réserver plus de 12 places.')
        return render_template('booking.html', club=club, competition=competition)




# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


if __name__ == "__main__":
    # debug=true permet d'obtenir plus d'informations en cas d'erreur
    app.run(debug=True)
