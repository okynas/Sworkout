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
  PRIMARY KEY (`id`)
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

CREATE TABLE IF NOT EXISTS `session` (
  `workout_id` INT(11) NOT NULL,
  `exercise_id` INT(11) NOT NULL,
  `workout_date` DATE NOT NULL,
  `workout_time` TIME NULL,
  `user_id` INT(11) NOT NULL,
  PRIMARY KEY (`workout_id`, `exercise_id`, `user_id` , `workout_date`),
  INDEX `fk_session1_exercise_idx` (`exercise_id` ASC) VISIBLE,
  INDEX `fk_session1_workout_idx` (`workout_id` ASC) VISIBLE,
  INDEX `fk_session1_user_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_session1_workout`
    FOREIGN KEY (`workout_id`)
    REFERENCES `workout` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_session1_exercise`
    FOREIGN KEY (`exercise_id`)
    REFERENCES `exercise` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_session1_user_idx`
    FOREIGN KEY (`user_id`)
    REFERENCES `user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- CREATE TABLE IF NOT EXISTS `session_has_user` (
--   `workout_id` INT(11) NOT NULL,
--   `exercise_id` INT(11) NOT NULL,
--   `user_id` INT(11) NOT NULL,
--   PRIMARY KEY (`session_workout_id`, `session_exercise_id`, `user_id`),
--   INDEX `fk_session_has_user_user1_idx` (`user_id` ASC) VISIBLE,
--   INDEX `fk_session_has_user_session1_idx` (`session_workout_id` ASC, `session_exercise_id` ASC) VISIBLE,
--   CONSTRAINT `fk_session_has_user_session1`
--     FOREIGN KEY (`session_workout_id` , `session_exercise_id`)
--     REFERENCES `session` (`workout_id` , `exercise_id`)
--     ON DELETE NO ACTION
--     ON UPDATE NO ACTION,
--   CONSTRAINT `fk_session_has_user_user1`
--     FOREIGN KEY (`user_id`)
--     REFERENCES `sworkout`.`user` (`id`)
--     ON DELETE NO ACTION
--     ON UPDATE NO ACTION)
-- ENGINE = InnoDB;

-- TEST DATA: USER WITH USERNAME: admin AND PASSWORD: admin
INSERT IGNORE INTO `user` (`username`,`first_name`,`last_name`,`email`,`password`,`is_admin`,`is_confirmed`,`created_at`,`updated_at`)
VALUES ("admin", "admin", "admin", "admin@okynas.com", "$2b$12$yBablCOZRNlmU0F6sUdAIOIxRS3jj1Xl../9OSQTEOCOM5a9Cxj9y", 0, 0, NOW(), NOW());

insert ignore into `exercise`(`id`, `name`, `image`, `difficulty`, `created_at`, `updated_at`)
values (1, "Benchpress", "", 3, NOW(), NOW());

insert ignore into `workout`(`id`, `repetition`, `set`, `weight`, `created_at`, `updated_at`)
values (1, 10, 3, 3, NOW(), NOW());

insert ignore into `session` (`workout_id`, `exercise_id`, `workout_date`, `workout_time`, `user_id`)
values(1, 1, NOW(), NOW(), 2);

-- insert ignore into `session_has_user`(`workout_id`, `exercise_id`, `user_id`)
-- values (1,1,1);
