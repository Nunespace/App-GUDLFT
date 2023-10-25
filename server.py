import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for

# import pdb
# import logging

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


def is_past_competition(date_str):
    """Vérife si la compétition est passée"""
    format = '%Y-%m-%d %H:%M:%S'
    date = datetime.strptime(date_str, format)
    return date > datetime.now()


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
for competition in competitions:
    competition['purchased_places'] = []
clubs = loadClubs()

@app.route('/')
def index():
    """Affiche la page d'accueil avec le tableau d'affichage des points"""
    #print("clubs ds server.py :", clubs)
    return render_template('index.html', clubs=clubs)

@app.route('/showSummary', methods=['POST'])
def showSummary():
    list_valid_email = [club['email'] for club in clubs]
    error = None
    # ajout de la vérification de l'email
    if request.form['email'] not in list_valid_email:
        error = "This email is not valid."
        return render_template('index.html', error=error, clubs=clubs)
    else:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        # ajout dans le doctionnaire competition de la clé club_name correspondant au nb de places déjà réservées
        for competition in competitions:
            competition.setdefault('past', is_past_competition(competition['date']))
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
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])
    club["points"] = int(club["points"])
    # ajout dans le dictionnaire competition de la clé club_name correspondant au nb de places déjà réservées
    competition.setdefault(club_name, 0)
    print("places réservées avant:", competition[club_name])
    placesRequired = int(request.form['places'])
    # ajout d'un if/else et maj des points
    if placesRequired > 12 or competition[club_name] == 12:
        flash('You cannot book more than 12 places per competition.')
        return render_template('booking.html', club=club, competition=competition)
    elif placesRequired > int(club["points"]):
        flash(f'You cannot book more than your points available ({club["points"]} points).')
        return render_template('booking.html', club=club, competition=competition)
    else:
        competition['numberOfPlaces'] -= placesRequired
        print("clubs ds server.py :", clubs)
        club["points"] -= placesRequired
        competition[club_name] += placesRequired
        print("places réservées après :", competition[club_name])
        print("clubs ds server.py2 :", clubs)
        flash('Great-booking complete!')
        #print("args ds l'url, méthode http, route demandée:", request.args, request.method, request.path)
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


if __name__ == "__main__":
    # debug=true permet d'obtenir plus d'informations en cas d'erreur
    app.run(debug=True)