




def test_root(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "message" in response.json()


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy"
    }


def test_create_employee(client):
    response = client.post(
        "/employees/",
        json={
            "name": "Test Employee",
            "email": "test.employee3@example.com",
            "department": "Engineering",
            "salary": 90000,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Test Employee"
    assert data["email"] == "test.employee3@example.com"
    assert data["department"] == "Engineering"
    assert data["salary"] == 90000


def test_get_employees(client):
    response = client.get("/employees/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_employee_not_found(client):
    response = client.get("/employees/999999")

    assert response.status_code == 404


    def test_update_employee():
        response = client.put(
            "/employees/1",
            json={
                "name": "Updated Employee",
                "email": "updated.employee@example.com",
                "department": "Backend",
                "salary": 100000,
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["name"] == "Updated Employee"
        assert data["email"] == "updated.employee@example.com"
        assert data["department"] == "Backend"
        assert data["salary"] == 100000


def test_delete_employee(client):
    create_response = client.post(
        "/employees/",
        json={
            "name": "Employee To Delete",
            "email": "employee.to.delete@example.com",
            "department": "Engineering",
            "salary": 70000,
        },
    )

    assert create_response.status_code == 200

    employee_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/employees/{employee_id}"
    )

    assert delete_response.status_code == 200

    assert delete_response.json() == {
        "message": "Employee deleted successfully"
    }

    get_response = client.get(
        f"/employees/{employee_id}"
    )

    assert get_response.status_code == 404

def test_invalid_email(client):
    response = client.post('/employees/',
                           json = {
                               'name' : 'Invalid Email',
                               'email' :'Noot an email',
                               'department' : 'Engineering',
                               'salary': 90000
                           })
    assert response.status_code == 422



def test_invalid_salary(client):
    response = client.post('/employees/',
                           json = {
                               'name':'Invalid Salary',
                               'email' :'invalidsalary@gmail.com',
                               'department' :'Engineering',
                               'salary' : -90000
                           })
    assert response.status_code == 422
    
def test_duplicate_email(client):

    email = "duplicate.test1@example.com"

    response1 = client.post('/employees/',
                           json={
                                 "name": "First Employee",
                                    "email": email,
                                    "department": "Engineering",
                                    "salary": 80000,
                           })
    
    assert response1.status_code == 200

    response2 = client.post('/employees/',
                           json={
                                 "name": "Second Employee",
                                    "email": email,
                                    "department": "Engineering",
                                    "salary": 80000,
                           })
    
    assert response2.status_code == 409
    assert response2.json()["detail"] == "Employee already exists"
    