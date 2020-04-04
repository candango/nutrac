-- Creating default schema

GRANT ALL ON SCHEMA public TO <NUTRAC_USER>;

-- ## SEQUENCES ##

DROP TABLE IF EXISTS profile;
DROP TABLE IF EXISTS nuser;
DROP SEQUENCE IF EXISTS instance_id_seq;
DROP SEQUENCE IF EXISTS nuser_id_seq;

CREATE SEQUENCE instance_id_seq;
GRANT ALL ON SEQUENCE instance_id_seq TO <NUTRAC_USER>;

CREATE SEQUENCE nuser_id_seq;
GRANT ALL ON SEQUENCE nuser_id_seq TO <NUTRAC_USER>;


CREATE TABLE instance(
  id                          BIGINT NOT NULL DEFAULT
    nextval('instance_id_seq'::regclass),
  uuid                        UUID NOT NULL,
);

GRANT ALL ON TABLE instance TO <NUTRAC_USER>;


-- ## User table ##
-- Added the i before as user is a reserved word in postgres.
CREATE TABLE nuser (
    id                          BIGINT NOT NULL DEFAULT
        nextval('nuser_id_seq'::regclass),
    uuid                        UUID NOT NULL,
    username                    CHARACTER VARYING(100) NOT NULL,
    password                    CHARACTER VARYING(255) NOT NULL,
    email                       CHARACTER VARYING(255),
    email1                      CHARACTER VARYING(255),
    unconfirmed_email           CHARACTER VARYING(255),
    confirm_email_token         CHARACTER VARYING(120),
    reset_password_token        CHARACTER VARYING(120),
    login_count                 INT NOT NULL DEFAULT 0,
    current_login_ip            CHARACTER VARYING(50),
    last_login_ip               CHARACTER VARYING(50),
    language                    CHARACTER VARYING(15)  NOT NULL DEFAULT 'en',
    getting_started             BOOLEAN NOT NULL DEFAULT FALSE,
    private_key                 TEXT NOT NULL,
    enabled                     BOOLEAN NOT NULL DEFAULT TRUE,
    deleted                     BOOLEAN NOT NULL DEFAULT FALSE,
    created_at                  TIMESTAMP with time zone NOT NULL
        DEFAULT CURRENT_TIMESTAMP,
    modified_at                 TIMESTAMP with time zone NOT NULL
        DEFAULT CURRENT_TIMESTAMP,
    deleted_at                  TIMESTAMP with time zone,
    reset_password_sent_at      TIMESTAMP with time zone,
    last_seen_at                TIMESTAMP with time zone,
    CONSTRAINT iuser_pk PRIMARY KEY (id),
    CONSTRAINT iuser_uuid_idx UNIQUE (uuid),
    CONSTRAINT iuser_username_idx UNIQUE (username),
    CONSTRAINT iuser_email_idx UNIQUE (email)
);

GRANT ALL ON TABLE nuser TO <NUTRAC_USER>;


-- ## Profile table ##
-- Holds the .
-- Country codes: https://www.worldatlas.com/aatlas/ctycodes.htm
CREATE TABLE profile (
    user_id                     BIGINT NOT NULL,
    company_name                CHARACTER VARYING(120),
    first_name                  CHARACTER VARYING(120),
    middle_name                 CHARACTER VARYING(120),
    last_name                   CHARACTER VARYING(120),
    address1                    CHARACTER VARYING(180),
    address2                    CHARACTER VARYING(180),
    city                        CHARACTER VARYING(120),
    zipcode                     CHARACTER VARYING(30),
    country                     CHARACTER VARYING(2),
    phone1                      CHARACTER VARYING(18),
    phone2                      CHARACTER VARYING(18),
    deleted                     BOOLEAN NOT NULL DEFAULT FALSE,
    created_at                  TIMESTAMP with time zone NOT NULL
        DEFAULT CURRENT_TIMESTAMP,
    modified_at                 TIMESTAMP with time zone NOT NULL
        DEFAULT CURRENT_TIMESTAMP,
    deleted_at                  TIMESTAMP with time zone,
    CONSTRAINT profile_pk PRIMARY KEY (user_id),
    CONSTRAINT profile_user_id_fk FOREIGN KEY(user_id)
        REFERENCES nuser(id) MATCH SIMPLE
        ON UPDATE RESTRICT ON DELETE RESTRICT
);

GRANT ALL ON TABLE profile TO <NUTRAC_USER>;
