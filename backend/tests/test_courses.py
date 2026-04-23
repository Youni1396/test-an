def _make_teacher(client):
    return client.post("/teachers", json={"name": "T", "subject": "S"}).json()


def test_create_course_requires_existing_teacher(client):
    resp = client.post("/courses", json={"name": "Algebra", "teacher_id": 999})
    assert resp.status_code == 400


def test_create_and_list_courses(client):
    teacher = _make_teacher(client)
    resp = client.post("/courses", json={"name": "Algebra", "teacher_id": teacher["id"]})
    assert resp.status_code == 201
    assert resp.json()["teacher_id"] == teacher["id"]

    resp = client.get("/courses")
    assert len(resp.json()) == 1


def test_update_course(client):
    teacher = _make_teacher(client)
    course = client.post("/courses", json={"name": "Algebra", "teacher_id": teacher["id"]}).json()
    resp = client.patch(f"/courses/{course['id']}", json={"name": "Geometry"})
    assert resp.status_code == 200
    assert resp.json()["name"] == "Geometry"


def test_delete_course(client):
    teacher = _make_teacher(client)
    course = client.post("/courses", json={"name": "Algebra", "teacher_id": teacher["id"]}).json()
    assert client.delete(f"/courses/{course['id']}").status_code == 204
    assert client.get(f"/courses/{course['id']}").status_code == 404
