CREATE TABLE IF NOT EXISTS java_zoekterm
(
    id BIGSERIAL PRIMARY KEY,
    zoekterm varchar NOT NULL,
    categorie varchar NOT NULL,
    "package" varchar,
    opmerking varchar,
    CONSTRAINT zoekterm_uk UNIQUE (zoekterm)
)

TABLESPACE pg_default;

GRANT SELECT, REFERENCES ON TABLE java_zoekterm TO appl;
GRANT USAGE ON SEQUENCE java_zoekterm_id_seq TO appl;
