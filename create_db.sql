CREATE TYPE SEX AS ENUM ('female', 'male', 'unknown');

CREATE TABLE "user" (
  id           SERIAL PRIMARY KEY,
  google_id    VARCHAR(255) UNIQUE,
  is_volunteer BOOL         NOT NULL,
  is_admin     BOOL         NOT NULL,
  name         VARCHAR(100) NOT NULL,
  email        VARCHAR(255) NOT NULL,
  UNIQUE (google_id, email)
);

CREATE TABLE location (
  id          SERIAL PRIMARY KEY,
  name        VARCHAR(255) NOT NULL,
  description TEXT,
  parent_id   INTEGER REFERENCES location (id)
);

CREATE TABLE dog (
  id          SERIAL PRIMARY KEY,
  is_hidden   BOOL NOT NULL,
  name        VARCHAR(255),
  sex         SEX  NOT NULL,
  description TEXT,
  is_adopted  BOOL NOT NULL,
  location_id INTEGER REFERENCES location (id) --has
);

CREATE TABLE add_request (
  id          SERIAL PRIMARY KEY,
  description TEXT,
  datetime    TIMESTAMPTZ,
  status      VARCHAR(100) NOT NULL, -- Should be archived
  comment     TEXT,
  user_id     INTEGER      NOT NULL REFERENCES "user" (id) --submits
);

CREATE TABLE inpayment (
  id      SERIAL PRIMARY KEY,
  amount  MONEY NOT NULL,
  comment TEXT,
  user_id INTEGER REFERENCES "user" (id) -- was_done_by
);

CREATE TABLE expenditure (
  id      SERIAL PRIMARY KEY,
  amount  MONEY NOT NULL, -- add check if can be negative
  comment TEXT
);

CREATE TABLE event_type (
  id             SERIAL PRIMARY KEY,
  type_name      VARCHAR(255) NOT NULL,
  is_significant BOOL         NOT NULL
);

CREATE TABLE event (
  id             SERIAL PRIMARY KEY,
  datetime       TIMESTAMPTZ NOT NULL, -- date + time + timezone
  description    TEXT,
  expenditure_id INTEGER REFERENCES expenditure (id), -- related with
  event_type_id  INTEGER     NOT NULL REFERENCES event_type (id), --is of
  dog_id         INTEGER     NOT NULL REFERENCES dog (id) --has
);

CREATE TABLE dog_picture (
  id         SERIAL PRIMARY KEY,
  uri        VARCHAR(1000) NOT NULL,
  dog_id     INTEGER REFERENCES dog (id), --dog has
  request_id INTEGER REFERENCES add_request (id) --request has
);

CREATE TABLE comment (
  index    SERIAL,
  text     TEXT        NOT NULL,
  datetime TIMESTAMPTZ NOT NULL,
  dog_id   INTEGER     NOT NULL REFERENCES dog (id), --has
  user_id  INTEGER     NOT NULL REFERENCES "user" (id) --leaves
);

CREATE TABLE adoption_request (
  user_id  INTEGER     NOT NULL REFERENCES "user" (id),
  dog_id   INTEGER     NOT NULL REFERENCES dog (id),
  comment  TEXT,
  datetime TIMESTAMPTZ NOT NULL,
  PRIMARY KEY (user_id, dog_id)
);