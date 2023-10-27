import pytest
from server import app


@pytest.fixture
def client():
    app.config.from_object({"TESTING": True})
    with app.test_client() as client:
        yield client


@pytest.fixture
def clubs_fixture():
    """Liste détaillée des clubs"""
    data = [
        {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
        {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
        {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "26"}
    ]
    return data


@pytest.fixture
def competitions_fixture():
    """Liste détaillée des compétitions"""
    data = [
        {
            "name": "Spring Festival",
            "date": "2024-03-27 10:00:00",
            "numberOfPlaces": "25",
        },
        {"name": "Fall Classic", "date": "2020-10-22 13:30:00", "numberOfPlaces": "3"},
        {"name": "Fall Classic full", "date": "2024-10-22 13:30:00", "numberOfPlaces": "0"},
    ]
    return data


@pytest.fixture
def competitions_fixture_with_purchased_places(clubs_fixture, competitions_fixture):
    """Liste des compétitions"""
    for competition in competitions_fixture:
        for club in clubs_fixture:
            club_name = club["name"]
            competition[club_name] = 12
    return competitions_fixture
