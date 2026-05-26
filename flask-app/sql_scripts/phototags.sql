DROP TABLE IF EXISTS phototags;

CREATE TABLE phototags (
 photoid integer references photos(photoid),
 tagid integer references tags(tagid),
 primary key (photoid, tagid)
 );
