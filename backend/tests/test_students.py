def _make_course(client):
    teacher = client.post("/teachers", json={"name": "T", "subject": "S"}).json()
    return client.post("/courses", json={"name": "C", "teacher_id": teacher["id"]}).json()


def test_create_student_requires_existing_course(client):
    resp = client.post("/students", json={"name": "Alex", "age": 15, "course_id": 999})
    assert resp.status_code == 400


def test_create_and_get_student(client):
    course = _make_course(client)
    resp = client.post(
        "/students",
        json={"name": "Alex", "age": 15, "course_id": course["id"]},
    )
    assert resp.status_code == 201
    student = resp.json()
    assert student["name"] == "Alex"

    resp = client.get(f"/students/{student['id']}")
    assert resp.status_code == 200


def test_update_student(client):
    course = _make_course(client)
    student = client.post(
        "/students",
        json={"name": "Alex", "age": 15, "course_id": course["id"]},
    ).json()
    resp = client.patch(f"/students/{student['id']}", json={"age": 16})
    assert resp.status_code == 200
    assert resp.json()["age"] == 16


def test_delete_student(client):
    course = _make_course(client)
    student = client.post(
        "/students",
        json={"name": "Alex", "age": 15, "course_id": course["id"]},
    ).json()
    assert client.delete(f"/students/{student['id']}").status_code == 204
    assert client.get(f"/students/{student['id']}").status_code == 404
