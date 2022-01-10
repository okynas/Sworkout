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
  `repetition` INTEGER,
  `set` INTEGER,
  `weight` INTEGER,
  `done` BOOLEAN,
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
  `workout_id` INT(11) NOT NULL,
  `workout_date` DATE NOT NULL,
  `workout_time` TIME NULL,
  `user_id` INT(11) NOT NULL,
  PRIMARY KEY (`workout_id`, `user_id` , `workout_date`)
ENGINE = InnoDB;


-- TEST DATA: USER WITH USERNAME: admin AND PASSWORD: Administrat0r!
INSERT IGNORE INTO `user` (`username`,`first_name`,`last_name`,`email`, `phone`, `password`,`is_admin`,`is_confirmed`,`created_at`,`updated_at`)
VALUES ("admin", "admin", "admin", "admin@okynas.com", 90089885, "$2b$12$jTMqgw8bRpa4dD87vnLO7uRaUnU1fdQq3HZD9U9GE6X9ZzI.2tnoi", 0, 0, NOW(), NOW());

insert ignore into `exercise`(`id`, `name`, `image`, `difficulty`, `created_at`, `updated_at`)
values (1, "Benchpress", "", 3, NOW(), NOW());

insert ignore into `workout`(`id`, `repetition`, `set`, `weight`, `created_at`, `updated_at`)
values (1, 10, 3, 3, NOW(), NOW());

insert ignore into `session` (`workout_id`, `exercise_id`, `workout_date`, `workout_time`, `user_id`)
values(1, 1, NOW(), NOW(), 2);
