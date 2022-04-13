def test_open_docs_page(client):
    response = client.get("docs/")
    assert response.status_code == 200


def test_get_404_if_page_does_not_exist(client):
    response = client.get("THIS/PAGE/DOES/NOT/EXIST")
    assert response.status_code == 404
