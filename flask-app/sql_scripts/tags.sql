DROP TABLE IF EXISTS tags;

CREATE TABLE tags (
 tagid serial primary key,
 tagname text UNIQUE
 );
