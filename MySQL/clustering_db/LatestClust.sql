-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema clusteringdb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema clusteringdb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `clusteringdb` DEFAULT CHARACTER SET utf8mb3 ;
USE `clusteringdb` ;

-- -----------------------------------------------------
-- Table `clusteringdb`.`clustdata`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clusteringdb`.`clustdata` (
  `Vector` LONGBLOB NULL DEFAULT NULL,
  `TSNE` LONGBLOB NULL DEFAULT NULL,
  `SVD` LONGBLOB NULL DEFAULT NULL,
  `DataSet` VARCHAR(100) NOT NULL,
  `Name` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`DataSet`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `clusteringdb`.`clustresult`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clusteringdb`.`clustresult` (
  `Labels` LONGBLOB NULL DEFAULT NULL,
  `command` VARCHAR(100) NOT NULL,
  `JobID` VARCHAR(100) NOT NULL,
  `DataSet` VARCHAR(100) NULL DEFAULT NULL,
  PRIMARY KEY (`JobID`),
  INDEX `Dataset_idx` (`DataSet` ASC) VISIBLE,
  CONSTRAINT `Dataset`
    FOREIGN KEY (`DataSet`)
    REFERENCES `clusteringdb`.`clustdata` (`DataSet`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `clusteringdb`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clusteringdb`.`users` (
  `Username` VARCHAR(45) NOT NULL,
  `Paswd` VARCHAR(45) NOT NULL,
  `UserID` INT NOT NULL,
  PRIMARY KEY (`UserID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
