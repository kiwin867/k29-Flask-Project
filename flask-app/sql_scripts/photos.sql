DROP TABLE IF EXISTS photos;

CREATE TABLE photos (
 photoid serial primary key,
 albumid integer references albums(albumid),
 phdata bytea,
 phname text,
 doc date
 );
