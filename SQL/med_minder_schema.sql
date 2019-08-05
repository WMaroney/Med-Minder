SET foreign_key_checks = 0;
drop table if exists users;
create table users (
	user_id integer primary key auto_increment,
	user_email varchar(255)unique key not null,,
	user_password varchar(255)
);

drop table if exists usermeds;
create table usermeds (
	med_id integer primary key auto_increment,
	user_id integer,
	med_name varchar(255),
	med_freq varchar(255),
	med_dose varchar(255),
	dr_name varchar(255),
	refill_date varchar(255),
	num_refills integer
);
ALTER TABLE usermeds ADD FOREIGN KEY (user_id) references users(user_id);
SET foreign_key_checks = 1;
