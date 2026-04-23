def test_create_and_get_teacher(client):
    resp = client.post("/teachers", json={"name": "Ms. Ada", "subject": "Math"})
    assert resp.status_code == 201
    teacher = resp.json()
    assert teacher["name"] == "Ms. Ada"
    assert teacher["subject"] == "Math"
    assert "id" in teacher

    resp = client.get(f"/teachers/{teacher['id']}")
    assert resp.status_code == 200
    assert resp.json() == teacher


def test_list_teachers(client):
    client.post("/teachers", json={"name": "A", "subject": "X"})
    client.post("/teachers", json={"name": "B", "subject": "Y"})
    resp = client.get("/teachers")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_update_teacher(client):
    created = client.post("/teachers", json={"name": "A", "subject": "X"}).json()
    resp = client.patch(f"/teachers/{created['id']}", json={"subject": "History"})
    assert resp.status_code == 200
    assert resp.json()["subject"] == "History"
    assert resp.json()["name"] == "A"


def test_delete_teacher(client):
    created = client.post("/teachers", json={"name": "A", "subject": "X"}).json()
    assert client.delete(f"/teachers/{created['id']}").status_code == 204
    assert client.get(f"/teachers/{created['id']}").status_code == 404


def test_get_missing_teacher_returns_404(client):
    assert client.get("/teachers/999").status_code == 404
