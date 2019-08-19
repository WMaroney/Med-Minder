SET foreign_key_checks = 0;
drop table if exists users;
create table users (
	user_id integer auto_increment,
	user_email varchar(255)unique key not null,
	user_password varchar(255),
	PRIMARY KEY (user_id)
);

drop table if exists usermeds;
create table usermeds (
	med_id integer auto_increment,
	user_id integer,
	med_name varchar(255),
	med_freq varchar(255),
	med_dose varchar(255),
	dr_name varchar(255),
	refill_date varchar(255),
	num_refills integer,
	PRIMARY KEY (med-id),
	FOREIGN KEY fk_user(user_id) REFERENCES users(user_id)
	ON UPDATE CASCADE
	ON DELETE RESTRICT
);
SET foreign_key_checks = 1;

