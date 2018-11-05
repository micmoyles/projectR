create database projectR;
create table projectR.users ( name varchar(30), dob timestamp);
create user 'reader'@'%' identified by '1canR3ad';
grant select on projectR.* to 'reader'@'%;