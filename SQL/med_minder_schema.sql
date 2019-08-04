SET foreign_key_checks = 0;
drop table if exists users;
create table users (
	user_id integer primary key auto_increment,
	user_email varchar(255) not null,
	user_password varchar(255) not null
);

drop table if exists usermeds;
create table usermeds (
	med_id integer primary key auto_increment,
	user_id integer not null,
	med_name varchar(255) not null,
	med_freq varchar(255) not null,
	med_dose varchar(255) not null,
	dr_name varchar(255) not null,
	refill_date varchar(255) not null,
	num_refills integer not null
);
ALTER TABLE usermeds ADD FOREIGN KEY (user_id) references users(user_id);
SET foreign_key_checks = 1;
