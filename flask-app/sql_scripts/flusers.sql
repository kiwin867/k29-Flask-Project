DROP TABLE IF EXISTS flusers;

CREATE TABLE flusers (
 id serial primary key,
 fname text,
 lname text,
 email varchar(20) unique,
 pass varchar(12) unique,
 photo bytea,
 dob date
 );
