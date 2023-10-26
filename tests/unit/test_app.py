import server
from server import is_past_competition


class TestHomePage:
    def test_get_home_page(self, mocker, client, clubs_fixture):
        mocker.patch.object(server, "clubs", clubs_fixture)
        response = client.get("/")
        assert response.status_code == 200

    def test_points_display_board(self, mocker, client, clubs_fixture):
        mocker.patch.object(server, "clubs", clubs_fixture)
        response = client.get("/")
        # Permet de décoder la data dans la requête
        data = response.data.decode()
        for club in clubs_fixture:
            assert club["name"] in data
            assert club["points"] in data

    def test_access_denied(self, client):
        invalid_email = "dupont@gmailcom"
        response = client.post("/showSummary", data={"email": invalid_email})
        data = response.data.decode()
        assert response.status_code == 200
        assert "This email is not valid." in data

    def test_logout(self, client):
        response = client.get("/logout")
        assert response.status_code == 302


class TestSummary:
    def test_get_summary_with_buttun_book(
        self, mocker, client, clubs_fixture, competitions_fixture
    ):
        """Vérifie le code réponse HTTP 200 et la présence du bouton book pour les compétitions à venir"""
        mocker.patch.object(server, "competitions", competitions_fixture)
        mocker.patch.object(server, "clubs", clubs_fixture)
        email = clubs_fixture[0]["email"]
        response = client.post("/showSummary", data={"email": email})
        data = response.data.decode()
        assert response.status_code == 200
        assert "book" in data

    def test_get_summary_without_buttun_book(
        self, mocker, client, clubs_fixture, competitions_fixture
    ):
        """
        Vérifie le code réponse HTTP 200 et l'absence du bouton book en cas de compétitions passées ou de places à 0
        """
        mocker.patch.object(server, "competitions", competitions_fixture[1:3])
        mocker.patch.object(server, "clubs", clubs_fixture)
        email = clubs_fixture[0]["email"]
        response = client.post("/showSummary", data={"email": email})
        data = response.data.decode()
        assert response.status_code == 200
        assert "book" not in data

    def test_past_competition(self, competitions_fixture):
        """teste la fonction qui détermine si la compétiton est à venir"""
        competitions_fixture[1]["date"] = "2024-03-27 10:00:00"
        date_str = competitions_fixture[1]["date"]
        expected = True
        assert is_past_competition(date_str) == expected


class TestBookPlaces:
    def test_get_book_page(self, mocker, client, competitions_fixture, clubs_fixture):
        """Quand l'utilisateur clique sur le boton book, alors la page de réservations doit s'ouvrir"""
        mocker.patch.object(server, "competitions", competitions_fixture)
        mocker.patch.object(server, "clubs", clubs_fixture)
        club = clubs_fixture[0]
        competition = competitions_fixture[1]
        url = f"/book/{competition['name']}/{club['name']}"
        response = client.get(url)
        assert response.status_code == 200

    def test_book_with_valid_places_required(
        self,
        mocker,
        client,
        clubs_fixture,
        competitions_fixture,
    ):
        """Teste le message de confirmation de l'achat ainsi que la mise à jour des points de club"""
        mocker.patch.object(server, "competitions", competitions_fixture)
        mocker.patch.object(server, "clubs", clubs_fixture)
        competition = competitions_fixture[0]
        club = clubs_fixture[0]
        placesRequired = 6
        data = {
            "club": club["name"],
            "competition": competition["name"],
            "places": placesRequired,
        }
        response = client.post("/purchasePlaces", data=data)
        data = response.data.decode()
        expected_message = "Great-booking complete!"
        expected_points_updates = int(club["points"]) - placesRequired
        assert expected_message in data
        assert str(expected_points_updates) in data

    def test_book_more_than_points_allowed(
        self, mocker, client, clubs_fixture, competitions_fixture
    ):
        mocker.patch.object(server, "competitions", competitions_fixture)
        mocker.patch.object(server, "clubs", clubs_fixture)
        competition = competitions_fixture[0]
        club = clubs_fixture[1]
        points = club["points"]
        # Achat d'une place en trop
        placesRequired = int(points) + 1
        data = {
            "club": club["name"],
            "competition": competition["name"],
            "places": placesRequired,
        }
        response = client.post("/purchasePlaces", data=data)
        data = response.data.decode()
        expected = f"You cannot book more than your points available ({points} points)."
        assert expected in data

    def test_book_more_than_12_places(
        self, mocker, client, clubs_fixture, competitions_fixture
    ):
        mocker.patch.object(server, "competitions", competitions_fixture)
        mocker.patch.object(server, "clubs", clubs_fixture)
        club = clubs_fixture[0]
        competition = competitions_fixture[0]
        club = clubs_fixture[0]
        placesRequired = 13
        data = {
            "club": club["name"],
            "competition": competition["name"],
            "places": placesRequired,
        }
        response = client.post("/purchasePlaces", data=data)
        data = response.data.decode()
        expected = "You cannot book more than 12 places per competition."
        assert expected in data
