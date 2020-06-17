create table alembic_version
(
    version_num VARCHAR(32) not null
        constraint alembic_version_pkc
            primary key
);

create table tenders
(
    tenderID                 INTEGER     not null
        primary key,
    tenderNumber             VARCHAR(25) not null
        unique,
    tenderDescription        VARCHAR(80) not null,
    category                 VARCHAR(40) not null,
    datePublished            VARCHAR(15) not null,
    closingDate              VARCHAR(15) not null,
    tenderStatus             VARCHAR(10) not null,
    nameOfInstitution        VARCHAR(60) not null,
    officalLocation          VARCHAR(60) not null,
    InstitutionContactPerson VARCHAR(60) not null,
    InstitutionPersonEmail   VARCHAR(60) not null,
    InstitutionPersonPhone   VARCHAR(60) not null,
    companyNames             JSON default '{}'
);

create table company
(
    companyID             INTEGER     not null
        primary key,
    companyName           VARCHAR(60) not null,
    companyRegistrationNo VARCHAR(50) not null,
    directors             VARCHAR(60) not null,
    companyPhoneNumber    VARCHAR(15) not null,
    companyAddress        VARCHAR(50) not null,
    applyCount            INTEGER
        unique,
    winningCount          INTEGER,
    isWinner              VARCHAR,
    awardedPoint          INTEGER,
    tenderNumber          VARCHAR(25) not null,
    tenderID              INTEGER
        references tenders
);

create table users
(
    id            INTEGER not null
        primary key,
    email         VARCHAR(60),
    username      VARCHAR(50),
    first_name    VARCHAR(60),
    last_name     VARCHAR(60),
    password_hash VARCHAR(128),
    is_admin      BOOLEAN,
    created_at    DATETIME,
    updated_at    DATETIME,
    check (is_admin IN (0, 1))
);

create unique index ix_users_email
    on users (email);

create index ix_users_first_name
    on users (first_name);

create index ix_users_last_name
    on users (last_name);

create unique index ix_users_username
    on users (username);


