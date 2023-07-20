# project/tests/test_summaries.py

import json


def test_create_summary(test_app_with_db):
    response = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "http://www.postcode.vip"})
    )

    assert response.status_code == 201
    assert response.json()["url"] == "http://www.postcode.vip"


def test_read_summary(test_app_with_db):
    response = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "http://www.postcode.vip"})
    )
    summary_id = response.json()["id"]

    test_app_with_db.get(f"/summaries/{summary_id}")

    assert response.status_code == 201

    response_dict = response.json()
    print("response_dict", response_dict)
    assert response_dict["id"] == summary_id
    assert response_dict["url"] == "http://www.postcode.vip"
    # assert response_dict["summary"]
    # assert response_dict["create_at"]


def test_read_all_summaries(test_app_with_db):
    response = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "http://testdriven.io"})
    )
    summary_id = response.json()["id"]

    response = test_app_with_db.get("/summaries/")

    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda d: d["id"] == summary_id, response_list))) == 1


def test_remove_summary(test_app_with_db):
    response = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "http://www.postcode.vip"})
    )
    summary_id = response.json()["id"]

    response = test_app_with_db.delete(f"/summaries/{summary_id}/")
    assert response.status_code == 200
    assert response.json() == {"id": summary_id, "url": "http://www.postcode.vip"}


def test_remove_summary_incorrect_id(test_app_with_db):
    response = test_app_with_db.delete("/summaries/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"

    response = test_app_with_db.delete("/summaries/0")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["path", "id"],
                "msg": "ensure this value is greater than 0",
                "type": "value_error.number.not_gt",
                "ctx": {"limit_value": 0},
            }
        ]
    }


def test_update_summary(test_app_with_db):
    response = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "http://www.postcode.vip"})
    )

    summary_id = response.json()["id"]

    test_app_with_db.put(
        f"/summaries/{summary_id}", data=json.dumps({"url": "http://www.baidu.vip"})
    )

    response_dict = response.json()
    print("response_dict", response_dict)
    assert response_dict["id"] == summary_id
    assert response_dict["url"] == "http://www.postcode.vip"
    # assert response_dict["summary"] == "updated!"
    # assert response_dict["created_at"]


def test_update_summary_incorrect_id(test_app_with_db):
    response = test_app_with_db.put(
        "/summaries/999/",
        data=json.dumps({"url": "http://www.postcode.vip", "summary": "updated!"}),
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"

    response = test_app_with_db.put(
        f"/summaries/0/",
        data=json.dumps({"url": "http://www.postcode.vip", "summary": "updated!"}),
    )
    assert response.status_code == 422

    assert response.json() == {
        "detail": [
            {
                "loc": ["path", "id"],
                "msg": "ensure this value is greater than 0",
                "type": "value_error.number.not_gt",
                "ctx": {"limit_value": 0},
            }
        ]
    }


def test_update_summary_invalid_json(test_app_with_db):
    response = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "http://www.postcode.vip"})
    )
    summary_id = response.json()["id"]

    response = test_app_with_db.put(f"/summaries/{summary_id}/", data=json.dumps({}))

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "url"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "summary"],
                "msg": "field required",
                "type": "value_error.missing",
            },
        ]
    }


def test_update_summary_invalid_keys(test_app_with_db):
    response = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://www.postcode.vip"})
    )

    summary_id = response.json()["id"]

    response = test_app_with_db.put(
        f"/summaries/{summary_id}", data=json.dumps({"url": "https://www.baidu.vip"})
    )

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "summary"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }

    response = test_app_with_db.put(
        f"/summaries/{summary_id}",
        data=json.dumps({"url": "invalid://case.vip", "summary": "0712yodated!"}),
    )

    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "URL scheme not permitted"


def test_read_summary_incorrect_id(test_app_with_db):
    response = test_app_with_db.get("/summaries/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"

    response = test_app_with_db.get("/summaries/0")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["path", "id"],
                "msg": "ensure this value is greater than 0",
                "type": "value_error.number.not_gt",
                "ctx": {"limit_value": 0},
            }
        ]
    }


def test_create_summaries_invalid_json(test_app):
    response = test_app.post("/summaries/", data=json.dumps({}))
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "url"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }

    response = test_app.post("/summaries/", data=json.dumps({"url": "invalid://url"}))
    print("response", response.json())
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "URL scheme not permitted"
