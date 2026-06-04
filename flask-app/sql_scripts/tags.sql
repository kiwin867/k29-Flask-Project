DROP TABLE IF EXISTS tags CASCADE;

CREATE TABLE tags (
 tagid serial primary key,
 tagname text UNIQUE
 );
