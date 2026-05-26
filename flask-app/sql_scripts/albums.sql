DROP TABLE IF EXISTS albums;

CREATE TABLE albums (
 albumid serial primary key,
 userid integer references flusers(id),
 alname text,
 doc date
 );
