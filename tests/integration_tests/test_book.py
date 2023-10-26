import pytest
import server



def test_get_summary(mocker, client, clubs_fixture, competitions_fixture):
    mocker.patch.object(server, "competitions", competitions_fixture)
    mocker.patch.object(server, "clubs", clubs_fixture)
    response = client.get("/")
    assert response.status_code == 200
    data = response.data.decode()
    for club in clubs_fixture:
        assert club["name"] in data
        assert club["points"] in data
    email = clubs_fixture[0]["email"]
    response = client.post("/showSummary", data={"email": email})
    data = response.data.decode()
    assert response.status_code == 200
    assert "book" in data
    response = client.get("/logout")
    assert response.status_code == 302


@pytest.mark.parametrize("placesRequired", [1,  12])
def test_book_places(mocker, client, competitions_fixture, clubs_fixture, placesRequired):
    mocker.patch.object(server, "competitions", competitions_fixture)
    mocker.patch.object(server, "clubs", clubs_fixture)
    club = clubs_fixture[0]
    email = club["email"]
    competition = competitions_fixture[0]
    url = f"/book/{competition['name']}/{club['name']}"
    response = client.post("/showSummary", data={"email": email})
    assert response.status_code == 200
    response = client.get(url)
    assert response.status_code == 200
    data = {
        "club": club["name"],
        "competition": competition["name"],
        "places": placesRequired,
    }
    response = client.post("/purchasePlaces", data=data)
    data = response.data.decode()
    expected_message = "Great-booking complete!"
    expected_points_updates = int(club['points'])
    assert expected_message in data
    assert str(expected_points_updates) in data
    response = client.get("/logout")
    assert response.status_code == 302


def test_book_places_more_than_total_max(mocker, client, competitions_fixture, clubs_fixture):
    """
    Quand si une secrétaire essaye de réserver plus de 12 places, même en plusieurs fois,
    alors la réservation n'est pas confirmée et un message doit apparaître
    """
    mocker.patch.object(server, "competitions", competitions_fixture)
    mocker.patch.object(server, "clubs", clubs_fixture)
    club = clubs_fixture[0]
    email = club["email"]
    competition = competitions_fixture[0]
    url = f"/book/{competition['name']}/{club['name']}"
    response = client.post("/showSummary", data={"email": email})
    placesRequired = 12
    response = client.get(url)
    data = {
        "club": club["name"],
        "competition": competition["name"],
        "places": placesRequired
    }
    response = client.post("/purchasePlaces", data=data)
    response = client.get(url)
    placesRequired = 1
    data = {
        "club": club["name"],
        "competition": competition["name"],
        "places": placesRequired}
    response = client.post("/purchasePlaces", data=data)
    data = response.data.decode()
    expected_message = "You cannot book more than 12 places per competition."
    assert expected_message in data
