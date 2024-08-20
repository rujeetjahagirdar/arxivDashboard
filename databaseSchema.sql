-- Create the schema
CREATE SCHEMA paper_monitoring;

-- Set the search path to include the newly created schema
SET search_path TO paper_monitoring;

-- Create the papers table
CREATE TABLE papers (
    id SERIAL PRIMARY KEY,
    arxiv_id VARCHAR(255),
    published TIMESTAMP,
    title TEXT,
    abstract TEXT,
    abs_link VARCHAR(255),
    pdf_link VARCHAR(255),
    journal_ref TEXT,
    comment TEXT,
    primary_category VARCHAR(255)
);

-- Create the authors table
CREATE TABLE authors (
    id SERIAL PRIMARY KEY,
    paper_id INTEGER REFERENCES papers(id),
    name VARCHAR(255)
);

-- Create the categories table
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    paper_id INTEGER REFERENCES papers(id),
    category VARCHAR(255)
);

-- Create the tags table
CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    paper_id INTEGER REFERENCES papers(id),
    tag VARCHAR(255)
);

-- Create the affiliations table
CREATE TABLE affiliations (
    id SERIAL PRIMARY KEY,
    paper_id INTEGER REFERENCES papers(id),
    affiliation VARCHAR(255)
);
