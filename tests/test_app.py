from src.app import activities


def test_root_redirects_to_static_index(client):
    expected_status = 307
    expected_location = "/static/index.html"

    response = client.get("/", follow_redirects=False)

    assert response.status_code == expected_status
    assert response.headers["location"] == expected_location


def test_get_activities_returns_all_activities(client):
    expected_keys = set(activities.keys())
    expected_count = 9

    response = client.get("/activities")

    body = response.json()
    assert response.status_code == 200
    assert isinstance(body, dict)
    assert len(body) == expected_count
    assert set(body.keys()) == expected_keys


def test_signup_for_activity_success(client):
    activity_name = "Chess Club"
    new_email = "new.student@mergington.edu"

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": new_email},
    )

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {new_email} for {activity_name}"}
    assert new_email in activities[activity_name]["participants"]


def test_signup_for_activity_duplicate_student(client):
    activity_name = "Chess Club"
    existing_email = activities[activity_name]["participants"][0]

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": existing_email},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up"}


def test_signup_for_activity_not_found(client):
    missing_activity = "Unknown Club"
    email = "student@mergington.edu"

    response = client.post(
        f"/activities/{missing_activity}/signup",
        params={"email": email},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_from_activity_success(client):
    activity_name = "Chess Club"
    existing_email = activities[activity_name]["participants"][0]

    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": existing_email},
    )

    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {existing_email} from {activity_name}"}
    assert existing_email not in activities[activity_name]["participants"]


def test_unregister_from_activity_student_not_registered(client):
    activity_name = "Chess Club"
    missing_email = "not.registered@mergington.edu"

    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": missing_email},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Student is not registered for this activity"}


def test_unregister_from_activity_not_found(client):
    missing_activity = "Unknown Club"
    email = "student@mergington.edu"

    response = client.delete(
        f"/activities/{missing_activity}/signup",
        params={"email": email},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}
