A one-liner phrase describing this project or app

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/0adca6e719a64b49bb8adea90dd1dc2d)](https://app.codacy.com/gh/BuildForSDG/team-279-Backend?utm_source=github.com&utm_medium=referral&utm_content=BuildForSDG/team-279-Backend&utm_campaign=Badge_Grade_Settings)
[![Codacy Badge](https://img.shields.io/badge/Code%20Quality-D-red)](https://img.shields.io/badge/Code%20Quality-D-red)
[![Code Health](https://landscape.io/github/BuildForSDG/team-279-Backend/master/landscape.svg?style=flat)](https://landscape.io/github/BuildForSDG/team-279-Backend)


## About

What is this project about. Ok to enrich here or the section above it with an image. 

Once this repo has been setup on Codacy by the TTL, replace the above badge with the actual one from the Codacy dashboard, and add the code coverage badge as well. This is mandatory

This is a simple python starter repo template for setting up your project. The setup contains:

- install: poetry via pip. poetry is a dependecy manager.

- poetry: configuration in pyproject.toml

- flake8: for linting and formatting

## Backend App and API
- It has the following relational entities:

    ``
    Tender
    ``
- It has endpoints to CREATE, UPDATE, and DELETE each entity in the application
- Only an authorized user can access the endpoints


## Why

Talk about what problem this solves, what SDG(s) and SGD targets it addresses and why these are important

## Usage
How would someone use what you have built, include URLs to the deployed app, service e.t.c when you have it setup

## Installation and Set Up

You should have **Python 3.5+** and **git** installed. 

1. Clone the repo you've created from the template herein and change into the directory

    ``
    git clone https://github.com/BuildForSDG/team-279-Backend
    ``

2. Change into repo directory by navigating into the root folder:

    ``
    cd team-279-Backend
    ``

3. Install poetry, a dependecy manager for python.

    On windows, you will need powershell to install it:

    ``
    (Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
    ``

    After that you will need to restart the shell to make it operational.

    &nbsp;

    On linux and other posix systems (mac included):

    ``
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
    ``

    &nbsp;

    To check that it is correctly installed, you can check the version:
    ``
    poetry --version
    ``

    May be the latest stable version is not installed with the installation script, to update poetry, you can run:

    ``
    poetry self update
    ``

4. With poetry installed, you should install project dependecies by running:

    ``
    poetry install
    ``

    This will install pytest for running tests and flake8, linter for your project.

#### To Note
`src/app.py` is the entry to the project and source code should go into the `src` folder.

## Testing
All tests should be written in the `tests` folder. tests/test_src.py is a sample test file that shows how tests should like. Feel free to delete it.

#### Hints

- Lint: `poetry run flake8`
- Run tests using the command: `poetry run pytest`
- Install dependencies: 
  `poetry add <dependency>`
- Install dev dependencies:
  `poetry add --dev <dev-dependency>`
- Run your project:
  `poetry run app`


## Database Setup
We create the MySQL database. Ensure you have MySQL installed and running, and then log in as the root user:

## Create dotenv
Create a `.env` file with the following keys:

    ```
    SECRET_KEY
    DATABASE_URI - for SQLAlchemy
    TEST_DATABASE_URI - for SQLAlchemy
    ENVIRONMENT - this is either production or development
    ```
## Database Migration
Initialize, migrate, and upgrade the database:

    ```
    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade
    ```

## Launching the Program
Run ```python __main__.py```. You may use [Postman](https://chrome.google.com/webstore/detail/postman/fhbjgbiflinjbdggehcddcbncdddomop?hl=en) for Google Chrome to run the API.

## API Endpoints

| Resource URL | Methods | Description | Requires Token |
| -------- | ------------- | --------- |--------------- |
| `/api/v1` | GET  | The index | FALSE |
| `/api/v1/auth/register` | POST  | User registration | FALSE |
|  `/api/v1/auth/login` | POST | User login | FALSE |
| `/api/v1/tenders` | GET, POST | View all tenders, add a tender | TRUE |
| `/api/v1/tenders/<string:id>` | GET, PUT, DELETE | View, edit, and delete a single tender | TRUE |

## Sample Tender API Requests

Registering and logging in to get a JWT token:
![User Registration]()

![User Login]()

Updating a tender:

![Updating Tender]()


## Built With
- [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.1/)
- [Flask](http://flask.pocoo.org/)
- [Flask-RESTful](http://flask-restful-cn.readthedocs.io/en/0.3.4/)


## Authors
List the team behind this project. Their names linked to their Github, LinkedIn, or Twitter accounts should suffice. Ok to signify the role they play in the project, including the TTL and mentor
1. Ajay Olabode [Github](https://github.com/boratonAJ) [LinkedIn](https://www.linkedin.com/in/boraton/) [TTL](https://github.com/orgs/BuildForSDG/teams/team-279)
 
## Contributing
If this project sounds interesting to you and you'd like to contribute, thank you!
First, you can send a mail to buildforsdg@andela.com to indicate your interest, why you'd like to support and what forms of support you can bring to the table, but here are areas we think we'd need the most help in this project :
1.  area one (e.g this app is about human trafficking and you need feedback on your roadmap and feature list from the private sector / NGOs)
2.  area two (e.g you want people to opt-in and try using your staging app at staging.project-name.com and report any bugs via a form)
3.  area three (e.g here is the zoom link to our end-of sprint webinar, join and provide feedback as a stakeholder if you can)

## Acknowledgements

Did you use someone else’s code?
Do you want to thank someone explicitly?
Did someone’s blog post spark off a wonderful idea or give you a solution to nagging problem?

It's powerful to always give credit.

## LICENSE
MIT