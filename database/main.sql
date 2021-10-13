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
  `exercise_id` INTEGER,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`exercise_id`) REFERENCES exercise(id)
) ENGINE=InnoDB;


CREATE TABLE IF NOT EXISTS `session` (
  `id` INTEGER AUTO_INCREMENT,
  `duration` INTEGER,
  `created_at` DateTime NOT NULL,
  `updated_at` DateTime NOT NULL,
  `workout_id` INTEGER NOT NULL,
  `user_id` INTEGER NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`workout_id`) REFERENCES workout(id),
  FOREIGN KEY (`user_id`) REFERENCES user(id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `user` (
  `id` INTEGER AUTO_INCREMENT,
  `username` VARCHAR(20) unique not null,
  `first_name` VARCHAR(20) not null,
  `last_name` VARCHAR(20) not null,
  `email` VARCHAR(120) unique not null,
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

CREATE TABLE IF NOT EXISTS `workout_has_user` (
  `workout_id` INT(11) NOT NULL,
  `user_id` INT(11) NOT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `duration` INT(11) NULL,
  PRIMARY KEY (`workout_id`, `user_id`),
  INDEX `fk_workout_has_user_user1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_workout_has_user_workout1_idx` (`workout_id` ASC) VISIBLE,
  CONSTRAINT `fk_workout_has_user_workout1`
    FOREIGN KEY (`workout_id`)
    REFERENCES `workout` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_workout_has_user_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- TEST DATA: USER WITH USERNAME: admin AND PASSWORD: admin
INSERT IGNORE INTO `user` (`username`,`first_name`,`last_name`,`email`,`password`,`is_admin`,`is_confirmed`,`created_at`,`updated_at`)
VALUES ("admin", "admin", "admin", "admin@okynas.com", "$2b$12$yBablCOZRNlmU0F6sUdAIOIxRS3jj1Xl../9OSQTEOCOM5a9Cxj9y", 0, 0, NOW(), NOW());

insert ignore into `exercise`(`id`, `name`, `image`, `difficulty`, `created_at`, `updated_at`)
values (1, "Benchpress", "", 3, NOW(), NOW());

insert ignore into `workout`(`id`, `repetition`, `set`, `weight`, `created_at`, `updated_at`, `exercise_id`)
values (1, 10, 3, 3, NOW(), NOW(), 1);

insert ignore into `workout_has_user` (`workout_id`, `user_id`, `created_at`, `updated_at`, `duration`)
values(1, 1, NOW(), NOW(), 100);
