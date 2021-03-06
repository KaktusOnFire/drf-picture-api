# drf-picture-api
API picture manager based on DRF+PostgreSQL

* [Setup](#setup)
* [Create admin account](#create-admin-account)
* [Running Tests](#running-tests)
* [Debug](#debug)
* [Documentation](#docs)
    * [Auth methods](#auth-methods)
    * [CRUD methods](#crud-methods)
    * [Utility methods](#utility-methods)
* [Request examples](#auth-request-examples)
    * [Auth request examples](#auth-request-examples)
    * [CRUD request examples](#crud-request-examples)
    * [Utility request examples](#utility-request-examples)

## Setup
```
docker-compose up
```

## Create admin account
```
docker exec -it api python manage.py createsuperuser
```

## Running tests
```
docker exec -it api python manage.py test
```

## Debug

Repository also includes a template for [Postman](https://www.postman.com/) for local tests.

## Docs
### Auth methods

| HTTP METHOD | POST            | GET       |
| ----------- | --------------- | --------- |
| /accounts/register | Create new user | - |
| /accounts/login | Create API token | - |
| /accounts/whoami | - | Get account information |

### CRUD methods

| HTTP METHOD | POST            | GET       | PUT         | DELETE |
| ----------- | --------------- | --------- | ----------- | ------ |
| CRUD OP     | CREATE          | READ      | UPDATE      | DELETE |
| /api/picture | Create new picture | Get all user pictures | - | - |
| /api/picture/:id | - | Get specific picture | Update picture | Delete picture |

### Utility methods

| HTTP METHOD | POST            | GET       | PUT         | DELETE |
| ----------- | --------------- | --------- | ----------- | ------ |
| /api/picture/purge | - | - | - | Delete all pictures in DB|

## Auth request examples

### POST /account/register

Request body:

    {
        'username': 'user',
        'password': 'password',
        'password2': 'password',
        'email': 'mail@gmail.ya',
        'first_name': 'Super',
        'last_name': 'User',
    }

### POST /account/login

Request body:

    {
        'username': 'user',
        'password': 'password',
    }

Response body:

    {
        "token": "1KVfv3VsmCCXyY5oITXkYJ5qwseDsmFc"
    }

### GET /account/whoami

Response body:

    {
        "id": 1,
        "first_name": "Super",
        "last_name": "User",
        "username": "user"
    }

## CRUD request examples

### POST /api/picture

Request body:

    {
        'image': FILE,
    }

### GET /api/picture

Response body:

    [
        {
            "id": 1,
            "image": "/media/pictures/0656f354303e4982b854b92792544b2a.jpg",
            "user": 1
        },
        {
            "id": 2,
            "image": "/media/pictures/52a211a49c3b460bbde114852eef8baa.jpg",
            "user": 1
        },
        {
            "id": 3,
            "image": "/media/pictures/64d9fff7b502445aadf7f932a97b3322.jpg",
            "user": 1
        }
    ]

### GET /api/picture/[id]

Response body:

    {
        'id': 1,
        'image': '/media/image.png',
        'user': 0,
    }

### POST /api/picture/[id]

Request body:

    {
        'image': FILE,
    }

Response body:

    {
        'id': 1,
        'image': '/media/new-image.png',
        'user': 0,
    }

### PUT /api/picture/[id]

Request body:

    {
        'image': FILE,
    }

Response body:

    {
        'id': 1,
        'image': '/media/new-image.png',
        'user': 0,
    }

### DELETE /api/picture/[id]

Response body:

    {"res": "Picture deleted!"}

## Utility request examples

### DELETE /api/picture/purge

Response body:

    {"res": 2 pictures deleted!"}
