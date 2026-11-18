def test_index_page_loads(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "Listo" in response.get_data(as_text=True)
    assert "proyecto base de la asignatura" in response.get_data(as_text=True)


def test_index_shows_login_links_to_anonymous_users(client):
    html = client.get("/").get_data(as_text=True)

    assert "Crear cuenta" in html
    assert "Mis tareas" not in html


def test_index_shows_account_and_logout_to_logged_users(logged_client, user):
    html = logged_client.get("/").get_data(as_text=True)

    assert user.name in html
    assert "Alumno" in html
    assert 'action="/auth/logout"' in html
    assert "Cerrar sesión" in html
