DROP TABLE IF EXISTS likes;

CREATE TABLE likes (
userid integer,
photoid integer,
 PRIMARY KEY (userid, photoid),
 FOREiGN KEY (userid) REFERENCES flusers(id),
 FOREIGN KEY (photoid) REFERENCES photos(photoid)
 );
