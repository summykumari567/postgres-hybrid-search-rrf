CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding VECTOR(1536),
    tsv tsvector
);

-- Full-text index
CREATE INDEX tsv_idx ON documents USING GIN(tsv);

-- Vector index
CREATE INDEX embedding_idx
ON documents
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Auto update tsvector
CREATE FUNCTION update_tsv() RETURNS trigger AS $$
BEGIN
  NEW.tsv := to_tsvector('english', NEW.content);
  RETURN NEW;
END
$$ LANGUAGE plpgsql;

CREATE TRIGGER tsv_update
BEFORE INSERT OR UPDATE ON documents
FOR EACH ROW EXECUTE FUNCTION update_tsv();