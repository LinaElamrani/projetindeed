DROP TABLE IF EXISTS jobs;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS applications;
DROP TABLE IF EXISTS companies;
DROP TABLE IF EXISTS categories;


CREATE TABLE users (
   user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    paswword TEXT NOT NULL,
    userstate TEXT NOT NULL
);


CREATE TABLE categories(
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name TEXT NOT NULL
);


CREATE TABLE companies (
  company_id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name TEXT NOT NULL
);

CREATE TABLE jobs (
    job_id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    location TEXT NOT NULL,
    postalcode TEXT NOT NULL,
    contract TEXT NOT NULL,
    worktime TEXT NOT NULL,
    userstate TEXT NOT NULL,
    description TEXT NOT NULL,
    salary TEXT NOT NULL,
    category_id INTEGER,
    company_id INTEGER,
    FOREIGN KEY(category_id) REFERENCES categories(category_id),
    FOREIGN KEY(company_id) REFERENCES companies(company_id)
);

CREATE TABLE applications (
    application_id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    numero TEXT NOT NULL,
    user_id INTEGER,
    job_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    FOREIGN KEY(job_id) REFERENCES jobs(job_id)
);
