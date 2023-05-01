set schema 'test';

-- Table: verwerk_project

DROP TABLE IF EXISTS verwerk_project;

CREATE TABLE IF NOT EXISTS verwerk_project
(
    id bigint NOT NULL,
    naam character varying COLLATE pg_catalog."default" NOT NULL,
    start_verwerking timestamp without time zone,
    einde_verwerking timestamp without time zone,
    processor character(36) COLLATE pg_catalog."default",
    status character varying COLLATE pg_catalog."default" NOT NULL DEFAULT 'nieuw'::character varying,
    resultaat character varying COLLATE pg_catalog."default",
    processtap character varying COLLATE pg_catalog."default",
    CONSTRAINT verwerk_project_pkey PRIMARY KEY (id),
    CONSTRAINT project_fkey FOREIGN KEY (id)
        REFERENCES project (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS verwerk_project
    OWNER to postgres;
   
ALTER TABLE verwerk_project ADD CONSTRAINT verwerk_project_fk FOREIGN KEY (processor) REFERENCES processor(identifier);


GRANT DELETE, INSERT, SELECT, UPDATE ON TABLE verwerk_project TO appl;

GRANT ALL ON TABLE verwerk_project TO postgres;

COMMENT ON TABLE verwerk_project
    IS 'Tabel om de status bij te houden van de verwerking. Status mag zijn: nieuw, gereed, bezig, geblokt. resultaat mag zijn <leeg>, gelukt, mislukt';