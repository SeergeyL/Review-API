# Reviews API

Reviews API collects users feedback on titles from different categories: books, music, films.
Users can leave their text reviews and leave comments under others reviews.

## Stack

- Django
- Django Rest Framework
- Django Simple JWT
- django-filter
- Docker


## Setup

Clone the repository and build the docker container.
```
docker build -t web .
```
Run container with project. Migrations will be automatically created. 
```
docker run -d --rm web
```
Create superuser.
```
docker exec <CONTAINER_ID> python manage.py createsuperuser
```
Run tests.
```
docker exec <CONTAINER_ID> pytest
```


## API
API documentation is available at `127.0.0.1/redoc`

User registration algorithm:

- Send request with *email* and *username* fields to `/auth/email/`
- API will send your confirmation code to your email. For testing purposes django `console.Email` backend is used. 
  Your confirmation code will be printed in console
  
- Send request to `/auth/token/` with your *email* and *confirmation_code*

### API Resources
- AUTH - user authentication
- USERS - registered users
- TITLES - available titles in api
- CATEGORIES - available categories in api
- GENRES - available genres in api
- REVIEWS - users reviews
- COMMENTS - users comments