from flask.testing import FlaskClient

from tests.forms import post_form

COMPARE_FORM = {
    "first_t_blast": "1000",
    "first_humidity": "10",
    "first_oxygen": "21",
    "first_gas": "0",
    "second_t_blast": "1200",
    "second_humidity": "15",
    "second_oxygen": "25",
    "second_gas": "8",
}


def test_compare_displays_both_temperatures_and_signed_difference(
    signed_in: FlaskClient,
) -> None:
    response = post_form(signed_in, "/compare", COMPARE_FORM)
    assert response.status_code == 200
    assert 'id="first-temperature">2201,0<' in response.text
    assert 'id="second-temperature">2080,0<' in response.text
    assert 'id="temperature-difference">-121,0<' in response.text


def test_compare_identifies_the_invalid_mode(signed_in: FlaskClient) -> None:
    response = post_form(signed_in, "/compare", COMPARE_FORM | {"second_gas": "99"})
    assert response.status_code == 400
    assert "Режим 2. Расход природного газа" in response.text
    assert 'id="first-temperature"' not in response.text
    assert 'name="second_gas" value="99"' in response.text
