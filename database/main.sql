create database if not exists `sworkout`;
use `sworkout`;

CREATE TABLE IF NOT EXISTS `exercise` (
  `id` INTEGER AUTO_INCREMENT,
  `name` VARCHAR(120),
  `image` VARCHAR(255),
  `difficulty` INTEGER,
  `created_at` DateTime NOT NULL,
  `updated_at` DateTime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `workout` (
  `id` INTEGER AUTO_INCREMENT,
  `exercise_id` INT(11) NOT NULL,
  `name` VARCHAR(255) unique not null,
  `repetition` INTEGER NOT NULL,
  `set` INTEGER NOT NULL,
  `weight` INTEGER NOT NULL,
  `done` BOOLEAN NOT NULL,
  `created_at` DateTime NOT NULL,
  `updated_at` DateTime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB;


CREATE TABLE IF NOT EXISTS `user` (
  `id` INTEGER AUTO_INCREMENT,
  `username` VARCHAR(20) unique not null,
  `first_name` VARCHAR(20) not null,
  `last_name` VARCHAR(20) not null,
  `email` VARCHAR(120) unique not null,
  `phone` INTEGER(8) unique not null,
  `password` VARCHAR(255) not null,
  `is_admin` BOOLEAN not null,
  `is_confirmed` BOOLEAN not null,
  `created_at` DateTime NOT NULL,
  `updated_at` DateTime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `recovery` (
  `id` INTEGER AUTO_INCREMENT,
  `email` VARCHAR(120) unique not null,
  `reset_code` VARCHAR(255) unique not null,
  `expires_in` DateTime NOT NULL,
  `created_at` DateTime NOT NULL,
  `updated_at` DateTime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `session` (
  `id` INTEGER AUTO_INCREMENT,
  `workout_date` DATE NOT NULL,
  `workout_time` TIME NULL,
  PRIMARY KEY (`id`)
)ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `userSessions` (
  `session_id` INT(11) NOT NULL,
  `user_id` INT(11) NOT NULL,
  PRIMARY KEY (`session_id`, `user_id`)
)ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `sessionWorkouts` (
  `session_id` INT(11) NOT NULL,
  `workout_id` INT(11) NOT NULL,
  PRIMARY KEY (`session_id`, `workout_id`)
)ENGINE = InnoDB;


-- TEST DATA: USER WITH USERNAME: admin AND PASSWORD: Administrat0r!
INSERT IGNORE INTO `user` (`username`,`first_name`,`last_name`,`email`, `phone`, `password`,`is_admin`,`is_confirmed`,`created_at`,`updated_at`)
VALUES ("admin", "admin", "admin", "admin@okynas.com", 90089885, "$2b$12$jTMqgw8bRpa4dD87vnLO7uRaUnU1fdQq3HZD9U9GE6X9ZzI.2tnoi", 0, 0, NOW(), NOW());

insert ignore into `exercise`(`id`, `name`, `image`, `difficulty`, `created_at`, `updated_at`)
values (1, "Benchpress", "", 3, NOW(), NOW());

insert ignore into `workout`(`id`, `name`, `exercise_id`, `repetition`, `set`, `weight`, `created_at`, `updated_at`)
values (1, "3-10-Benchpress", 1, 10, 3, 3, NOW(), NOW());

insert ignore into `session` (`id`, `workout_date`, `workout_time`)
values(1, NOW(), NOW());

insert ignore into `userSessions` (`user_id`, `session_id`)
values(1, 1);

insert ignore into `sessionWorkouts` (`workout_id`, `session_id`)
values(1, 1);

