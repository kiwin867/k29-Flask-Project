DROP TABLE IF EXISTS has_friend;

CREATE TABLE has_friend (
 flfid serial primary key,
 fid integer references flusers(id),
 fname text,
 lname text,
 email varchar(20) unique,
 pass varchar(12) unique,
 photo bytea,
 dob date
 );
