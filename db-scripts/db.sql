-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema studentmktplace_db
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema studentmktplace_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `studentmktplace_db` DEFAULT CHARACTER SET utf8 ;
USE `studentmktplace_db` ;

-- -----------------------------------------------------
-- Table `studentmktplace_db`.`user_role`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `studentmktplace_db`.`user_role` (
  `ur_id` INT NOT NULL AUTO_INCREMENT,
  `ur_name` VARCHAR(30) NOT NULL,
  PRIMARY KEY (`ur_id`),
  UNIQUE INDEX `ur_name_UNIQUE` (`ur_name` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `studentmktplace_db`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `studentmktplace_db`.`user` (
  `u_id` INT NOT NULL AUTO_INCREMENT,
  `u_name` VARCHAR(50) NOT NULL,
  `u_email` VARCHAR(50) NOT NULL,
  `u_password` VARCHAR(150) NOT NULL,
  `u_phone` VARCHAR(12) NULL,
  `u_address` VARCHAR(100) NULL,
  `u_postalCode` VARCHAR(6) NULL,
  `u_otp` INT(6) NULL,
  `u_emailVerified` TINYINT NOT NULL DEFAULT 0,
  `u_role` INT NOT NULL,
  PRIMARY KEY (`u_id`),
  UNIQUE INDEX `user_email_UNIQUE` (`u_email` ASC) VISIBLE,
  INDEX `user_role_idx` (`u_role` ASC) VISIBLE,
  CONSTRAINT `user_role`
    FOREIGN KEY (`u_role`)
    REFERENCES `studentmktplace_db`.`user_role` (`ur_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `studentmktplace_db`.`products_category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `studentmktplace_db`.`products_category` (
  `pc_id` INT NOT NULL,
  `pc_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`pc_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `studentmktplace_db`.`product_status`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `studentmktplace_db`.`product_status` (
  `ps_id` INT NOT NULL,
  `ps_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`ps_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `studentmktplace_db`.`products`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `studentmktplace_db`.`products` (
  `p_id` INT NOT NULL,
  `p_title` VARCHAR(100) NOT NULL,
  `p_description` VARCHAR(200) NOT NULL,
  `p_price` INT NULL,
  `p_address` VARCHAR(100) NULL,
  `p_category` INT NOT NULL,
  `p_userId` INT NOT NULL,
  `p_titImage` LONGBLOB NOT NULL,
  `p_status` INT NOT NULL DEFAULT 1,
  PRIMARY KEY (`p_id`),
  INDEX `category_id_fk_idx` (`p_category` ASC) VISIBLE,
  INDEX `user_id_fk_idx` (`p_userId` ASC) VISIBLE,
  INDEX `ps_id_fk_idx` (`p_status` ASC) VISIBLE,
  CONSTRAINT `category_id_fk`
    FOREIGN KEY (`p_category`)
    REFERENCES `studentmktplace_db`.`products_category` (`pc_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `user_id_fk`
    FOREIGN KEY (`p_userId`)
    REFERENCES `studentmktplace_db`.`user` (`u_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `ps_id_fk`
    FOREIGN KEY (`p_status`)
    REFERENCES `studentmktplace_db`.`product_status` (`ps_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

ALTER TABLE products MODIFY p_id INT AUTO_INCREMENT;

-- -----------------------------------------------------
-- Table `studentmktplace_db`.`favourites`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `studentmktplace_db`.`favourites` (
  `f_userId` INT NOT NULL,
  `f_productId` INT NOT NULL,
  INDEX `userId_fk_idx` (`f_userId` ASC) VISIBLE,
  INDEX `productId_fk_idx` (`f_productId` ASC) VISIBLE,
  CONSTRAINT `userId_fk`
    FOREIGN KEY (`f_userId`)
    REFERENCES `studentmktplace_db`.`user` (`u_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `productId_fk`
    FOREIGN KEY (`f_productId`)
    REFERENCES `studentmktplace_db`.`products` (`p_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `studentmktplace_db`.`product_images`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `studentmktplace_db`.`product_images` (
  `pi_productId` INT NOT NULL,
  `pi_primImage` LONGBLOB NOT NULL,
  `pi_secImage` LONGBLOB NULL,
  `pi_terImage` LONGBLOB NULL,
  INDEX `productId_fk_idx` (`pi_productId` ASC) VISIBLE,
  CONSTRAINT `prodId_fk`
    FOREIGN KEY (`pi_productId`)
    REFERENCES `studentmktplace_db`.`products` (`p_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

ALTER TABLE product_images add column pi_id int(10) primary key auto_increment;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

