# VTender Backend APP

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/0adca6e719a64b49bb8adea90dd1dc2d)](https://app.codacy.com/gh/BuildForSDG/team-279-Backend?utm_source=github.com&utm_medium=referral&utm_content=BuildForSDG/team-279-Backend&utm_campaign=Badge_Grade_Settings)
[![Codacy Badge](https://img.shields.io/badge/Code%20Quality-D-red)](https://img.shields.io/badge/Code%20Quality-D-red)
[![Code Health](https://landscape.io/github/BuildForSDG/team-279-Backend/master/landscape.svg?style=flat)](https://landscape.io/github/BuildForSDG/team-279-Backend)
[![Build Status](https://travis-ci.org/BuildForSDG/team-279-Backend.svg?branch=develop)](https://travis-ci.org/github/BuildForSDG/team-279-Backend)
[![Coverage Status](https://coveralls.io/repos/github/BuildForSDG/team-279-Backend/badge.svg)](https://coveralls.io/github/BuildForSDG/team-279-Backend)


## About

Over the past four years, a number of companies have lost tens of thousands of Rand due to alleged fraudulent request for quotations (RFQS). With this software, small medium and micro enterprises (SMME) can verify the authenticity of Tender(RFQS), and also assist bidders to detect corruption and discrepancies in an awarded tender.
vTender app is an intuitive web-based UI/UX that has mobile responsive frontend which allows users to verify tender, view list of valid tender(s), and detect awarded tender corruption.


The vTender app addresses the following SDG goals:

-   Provide inclusive for all people while substantially reduce corruption and bribery in Africa countries,as well as globally
-   Allows anyone, regardless of their literacy abilities, to verify/validate the request for quotation (RFQ) from Government departments/parastatals. 
-   Allows SMME's to understand how a particular tender is been awarded, as well as to detect discrepancies in an awarded tenders. 
-   Helps to prevent any act of frauds and corruptions based on an implemented algorithm. 

## Backend App and API

-   It has the following relational entities:
    ``
    Tender
    ``
-   It has endpoints to CREATE, UPDATE, and DELETE each entity in the application

-   Only an authorized user can access the endpoints

## Why

Talk about what problem this solves, what SDG(s) and SGD targets it addresses and why these are important

## Usage

How would someone use what you have built, include URLs to the deployed app, service e.t.c when you have it setup

## Installation and Set Up

1.  You should have **Python 3.5+** and **git** installed.
2.  To get started, clone this repository by using: `git clone https://github.com/BuildForSDG/team-279-Backend.git`
3.  Change to the root directory by navigating to the folder: `cd team-279-Backend`
4.  Install the required packages using Pipenv virtual environment: `Pipenv install`
5.  Create a `.env` file with the following keys:
    
    ```py
    SECRET_KEY

    DATABASE_URI - for SQLAlchemy

    TEST_DATABASE_URI - for SQLAlchemy

    ENVIRONMENT - this is either production or development
    ```
6.  Initialize, migrate, and upgrade the database:
    
    ```py
    python manage.py db init

    python manage.py db migrate

    python manage.py db upgrade
    ```
5.  Start by launching the flask server by running `python run.py`
6.  Navigate to `http://localhost:5000` in the browser to view the api.
7.  Alternatively, you may install [Postman](https://www.postman.com/) locally or You may use [Postman](https://chrome.google.com/webstore/detail/postman/fhbjgbiflinjbdggehcddcbncdddomop?hl=en) for Google Chrome to run the API.
8.  The following REST API URL endpoints can be use to test the program for quickly and easily access.

### API Endpoints

| Resource URL                                | Methods                 | Description                            | Requires Authorization |
| ------------------------------------------- | ----------------------- | -------------------------------------- | ---------------------- |
| `/api/v1`                                   | GET                     | The index                              | FALSE                  |
| `/api/v1/auth/register`                     | POST                    | User registration                      | FALSE                  |
|  `/api/v1/auth/login`                       | POST                    | User login                             | FALSE                  |
| `/api/v1/tenders`                           | GET, POST               | View all tenders, add a tender         | TRUE                   |
| `/api/v1/tenders/<string:tenderID>`         | GET, PUT, DELETE        | View, edit, and delete a single tender | TRUE                   |
| `/api/v1/company`                           | GET, POST               | View all tenders, add a company        | TRUE                   |
| `/api/v1/company/<string:companyID>`        | GET, PUT, DELETE        | View, edit, and delete a single company| TRUE                   |
| `/api/v1/combined-tenders`                  | GET                     | View                                   | TRUE                   |
| `/api/v1/one-tender/<string:tenderNumber>`  | GET                     | View                                   | TRUE                   |


## Postman Setup for testing the Program REST API 

Open this collection in postman by clicking the button below:

[![Run in Postman](https://run.pstmn.io/button.svg)](https://documenter.getpostman.com/view/10400114/SzzkcHBh?version=latest)

If you're using Postman for testing the REST api, you can use the following setup:

-   Make sure you have an environment set for your collection.

-   POST to `https://team-279-backend.herokuapp.com/api/v1/auth/register` and add your details to sign up

-   POST to `https://team-279-backend.herokuapp.com/api/v1/auth/login` to obtain token authorization

-   Paste this code in Tests which will save the token to the environment.

        var jsonData = JSON.parse(responseBody);
        postman.setEnvironmentVariable("token", jsonData.token);

-   In the Authorization section of your subsequent posts, set the Authorization type as Bearer Token and add {{token}}
    in the token section

## Heroku deployment

View the deployed application here [vTender API](https://team-279-backend.herokuapp.com/)   

## Tender API Requests

Registering and logging in to get a JWT token:

-   ![User Registration]()

-   ![User Login]()

Update a tender:

-   ![Updating Tender]()

Update a company:

-   ![Updating Company]()

To test the API

## Authors

-   [Ajay Olabode](https://github.com/boratonAJ) [LinkedIn](https://www.linkedin.com/in/boraton/) [TTL](https://github.com/orgs/BuildForSDG/teams/team-279)

## Contributing

If this project sounds interesting to you and you'd like to contribute, thank you!
First, you can send a mail to buildforsdg@andela.com to indicate your interest, why you'd like to support and what forms of support you can bring to the table, but here are areas we think we'd need the most help in this project :
1.  area one (e.g this app is about human trafficking and you need feedback on your roadmap and feature list from the private sector / NGOs)
2.  area two (e.g you want people to opt-in and try using your staging app at staging.project-name.com and report any bugs via a form)
3.  area three (e.g here is the zoom link to our end-of sprint webinar, join and provide feedback as a stakeholder if you can)

## Acknowledgements

-   [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.1/)

-   [Flask](http://flask.pocoo.org/)

-   [Flask-RESTful](http://flask-restful-cn.readthedocs.io/en/0.3.4/)

-   [Token-Based Authentication With Flask](https://realpython.com/token-based-authentication-with-flask/)

## LICENSE

MIT
