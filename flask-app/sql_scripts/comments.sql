DROP TABLE IF EXISTS comments CASCADE;

CREATE TABLE comments (
 commentid serial primary key,
 userid integer references flusers(id),
 photoid integer references photos(photoid),
 comment text,
 doc date
 );
