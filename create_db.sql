CREATE TYPE public.SEX AS ENUM ('female', 'male', 'unknown');

CREATE TABLE public."user" (
  id           SERIAL PRIMARY KEY,
  google_id    VARCHAR(255) UNIQUE,
  is_volunteer BOOL         NOT NULL,
  is_admin     BOOL         NOT NULL,
  _is_active    BOOL         NOT NULL,
  name         VARCHAR(100) NOT NULL,
  email        VARCHAR(255) NOT NULL,
  UNIQUE (google_id),
  UNIQUE (email)
);

CREATE TABLE public.location (
  id          SERIAL PRIMARY KEY,
  name        VARCHAR(255) NOT NULL,
  description TEXT,
  parent_id   INTEGER REFERENCES location (id)
);

CREATE TABLE public.dog (
  id          SERIAL PRIMARY KEY,
  is_hidden   BOOL NOT NULL,
  name        VARCHAR(255),
  sex         SEX  NOT NULL,
  description TEXT,
  is_adopted  BOOL NOT NULL,
  location_id INTEGER REFERENCES location (id) --has
);

CREATE TABLE public.add_request (
  id          SERIAL PRIMARY KEY,
  description TEXT         NOT NULL,
  datetime    TIMESTAMPTZ  NOT NULL,
  status      VARCHAR(100) NOT NULL, -- Should be archived
  comment     TEXT,
  user_id     INTEGER      NOT NULL REFERENCES "user" (id) --submits
);

CREATE TABLE public.inpayment (
  id       SERIAL PRIMARY KEY,
  amount   MONEY NOT NULL,
  datetime TIMESTAMPTZ  NOT NULL,
  comment  TEXT,
  user_id  INTEGER REFERENCES "user" (id) -- was_done_by
);

CREATE TABLE public.expenditure (
  id       SERIAL PRIMARY KEY,
  amount   MONEY NOT NULL, -- add check if can be negative
  datetime TIMESTAMPTZ  NOT NULL,
  comment  TEXT
);

CREATE TABLE public.event_type (
  id             SERIAL PRIMARY KEY,
  type_name      VARCHAR(255) NOT NULL,
  is_significant BOOL         NOT NULL
);

CREATE TABLE public.event (
  id             SERIAL PRIMARY KEY,
  datetime       TIMESTAMPTZ NOT NULL, -- date + time + timezone
  description    TEXT,
  expenditure_id INTEGER REFERENCES expenditure (id), -- related with
  event_type_id  INTEGER     NOT NULL REFERENCES event_type (id), --is of
  dog_id         INTEGER     NOT NULL REFERENCES dog (id) --has
);

CREATE TABLE public.dog_picture (
  id         SERIAL PRIMARY KEY,
  uri        VARCHAR(1000) NOT NULL,
  dog_id     INTEGER REFERENCES dog (id), --dog has
  request_id INTEGER REFERENCES add_request (id), --request has
  is_main    BOOL NOT NULL
  --TODO: Check query
);

CREATE TABLE public.comment (
  index    SERIAL,
  text     TEXT        NOT NULL,
  datetime TIMESTAMPTZ NOT NULL,
  dog_id   INTEGER     NOT NULL REFERENCES dog (id), --has
  user_id  INTEGER     NOT NULL REFERENCES "user" (id) --leaves
);

CREATE TABLE public.adoption_request (
  user_id  INTEGER     NOT NULL REFERENCES "user" (id),
  dog_id   INTEGER     NOT NULL REFERENCES dog (id),
  comment  TEXT,
  datetime TIMESTAMPTZ NOT NULL,
  PRIMARY KEY (user_id, dog_id)
);