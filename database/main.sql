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
  `repetition` INTEGER,
  `set` INTEGER,
  `weight` INTEGER,
  `created_at` DateTime NOT NULL,
  `updated_at` DateTime NOT NULL,
  `exercise_id` INTEGER NOT NULL
  PRIMARY KEY (`id`),
  FOREIGN KEY (`exercise_id`) REFERENCES exercise(id)
) ENGINE=InnoDB;


CREATE TABLE IF NOT EXISTS `session` (
  `id` INTEGER AUTO_INCREMENT,
  `duration` INTEGER,
  `created_at` DateTime NOT NULL,
  `updated_at` DateTime NOT NULL,
  `workout_id` INTEGER NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`workout_id`) REFERENCES workout(id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `user` (
  `id` INTEGER AUTO_INCREMENT,
  `username` VARCHAR(20) unique not null,
  `first_name` VARCHAR(20) not null,
  `last_name` VARCHAR(20) not null,
  `email` VARCHAR(120) unique not null,
  `password` VARCHAR(255) not null,
  `is_admin` BOOLEAN unique not null,
  `is_confirmed` BOOLEAN unique not null,
  `created_at` DateTime NOT NULL,
  `updated_at` DateTime NOT NULL,
  PRIMARY KEY (`id`),
) ENGINE=InnoDB;