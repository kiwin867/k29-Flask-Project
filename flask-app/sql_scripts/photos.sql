DROP TABLE IF EXISTS photos CASCADE;

CREATE TABLE photos (
 photoid serial primary key,
 albumid integer references albums(albumid),
 phdata bytea,
 phname text,
 doc date
 );
