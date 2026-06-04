DROP TABLE IF EXISTS flusers CASCADE;

CREATE TABLE flusers (
 id serial primary key,
 fname text,
 lname text,
 email varchar(30) unique,
 pass varchar(16),
 photo bytea,
 dob date
 );
