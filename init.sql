-- DDL generated by Postico 2.1
-- Not all database features are supported. Do not use for backup.

-- Table Definition ----------------------------------------------

CREATE TABLE quote (
    id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
    author character varying NOT NULL,
    quote character varying NOT NULL,
    created_at timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    freeform_date character varying
);

-- Indices -------------------------------------------------------

CREATE INDEX quote_author ON quote(author text_ops);