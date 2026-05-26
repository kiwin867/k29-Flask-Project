DROP TABLE IF EXISTS flfriends;

CREATE TABLE flfriends (
 flfid serial primary key,
 fid integer references flusers(id),
 fname text,
 lname text,
 email varchar(20)
 );
