DROP TABLE IF EXISTS likes;

CREATE TABLE likes (
 likeid serial primary key,
 userid integer references flusers(id),
 photoid integer references photos(photoid)
 );
