CREATE DATABASE  IF NOT EXISTS `reddit_parsing` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `reddit_parsing`;
-- MySQL dump 10.13  Distrib 8.0.32, for Win64 (x86_64)
--
-- Host: localhost    Database: reddit_parsing
-- ------------------------------------------------------
-- Server version	8.0.32

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `submission`
--

DROP TABLE IF EXISTS `submission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `submission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `url` varchar(768) NOT NULL COMMENT 'full url of the submission (varchar is used for unique constraint)',
  `full_name` varchar(768) NOT NULL COMMENT 'reddit-qualified full name (varchar is used for unique constraint)',
  `title` text COMMENT 'author-provided title',
  `text_body` text COMMENT 'possibly empty string of text',
  `author` text COMMENT 'reddit-qualified author of the submission',
  `upvotes` int NOT NULL COMMENT 'possitive votes',
  `downvotes` int DEFAULT NULL COMMENT 'negative votes',
  `created_timestamp` datetime NOT NULL COMMENT 'submission creation timestamp',
  `parsed_timestamp` datetime NOT NULL COMMENT 'timestamp when submission was parsed. For compliance with Reddit api licence',
  `flair` text COMMENT 'community defined flair, if available',
  `job_id` text NOT NULL COMMENT 'job id related to web app',
  PRIMARY KEY (`id`),
  UNIQUE KEY `url` (`url`),
  UNIQUE KEY `full_name` (`full_name`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `submission_comment`
--

DROP TABLE IF EXISTS `submission_comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `submission_comment` (
  `id` int NOT NULL AUTO_INCREMENT,
  `full_name` varchar(768) NOT NULL COMMENT 'reddit-qualified full name',
  `submission_name` varchar(768) NOT NULL COMMENT 'reddit-qualified full name',
  `text_body` text COMMENT 'possibly empty string of text',
  `author` text COMMENT 'reddit-qualified author of the submission',
  `upvotes` int NOT NULL COMMENT 'possitive votes',
  `downvotes` int DEFAULT NULL COMMENT 'negative votes',
  `created_timestamp` datetime NOT NULL COMMENT 'submission creation timestamp',
  `parsed_timestamp` datetime NOT NULL COMMENT 'timestamp when comment was parsed. For compliance with Reddit api licence',
  `job_id` text NOT NULL COMMENT 'job id related to web app',
  PRIMARY KEY (`id`),
  UNIQUE KEY `full_name` (`full_name`),
  KEY `FK_parent_submission_idx` (`submission_name`),
  CONSTRAINT `FK_parent_submission` FOREIGN KEY (`submission_name`) REFERENCES `submission` (`full_name`)
) ENGINE=InnoDB AUTO_INCREMENT=3494 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `subreddit`
--

DROP TABLE IF EXISTS `subreddit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subreddit` (
  `id` int NOT NULL AUTO_INCREMENT,
  `full_name` varchar(768) NOT NULL COMMENT 'reddit-qualified full name of subreddit',
  `display_name` text NOT NULL COMMENT 'user-visible name',
  `url` text NOT NULL COMMENT 'url of subreddit',
  `parsed_timestamp` datetime NOT NULL COMMENT 'timestamp when comment was parsed. For compliance with Reddit api licence',
  `job_id` text NOT NULL COMMENT 'job id related to web app',
  PRIMARY KEY (`id`),
  UNIQUE KEY `full_name` (`full_name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `subreddit_active_users`
--

DROP TABLE IF EXISTS `subreddit_active_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subreddit_active_users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `subreddit_full_name` varchar(256) NOT NULL COMMENT 'reddit-qualified full name of subreddit',
  `user_full_name` varchar(256) NOT NULL COMMENT 'reddit-qualified full name',
  `parsed_timestamp` datetime NOT NULL COMMENT 'timestamp when comment was parsed. For compliance with Reddit api licence',
  `job_id` text NOT NULL COMMENT 'job id related to web app',
  PRIMARY KEY (`id`),
  UNIQUE KEY `subreddit_full_name` (`subreddit_full_name`,`user_full_name`),
  CONSTRAINT `subreddit_active_users_ibfk_1` FOREIGN KEY (`subreddit_full_name`) REFERENCES `subreddit` (`full_name`)
) ENGINE=InnoDB AUTO_INCREMENT=642 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping events for database 'reddit_parsing'
--
/*!50106 SET @save_time_zone= @@TIME_ZONE */ ;
/*!50106 DROP EVENT IF EXISTS `delete_old_data` */;
DELIMITER ;;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;;
/*!50003 SET character_set_client  = utf8mb4 */ ;;
/*!50003 SET character_set_results = utf8mb4 */ ;;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;;
/*!50003 SET @saved_time_zone      = @@time_zone */ ;;
/*!50003 SET time_zone             = 'SYSTEM' */ ;;
/*!50106 CREATE*/ /*!50117 DEFINER=`root`@`localhost`*/ /*!50106 EVENT `delete_old_data` ON SCHEDULE EVERY 1 DAY STARTS '2024-03-18 22:47:06' ON COMPLETION NOT PRESERVE ENABLE DO CALL delete_rows_links() */ ;;
/*!50003 SET time_zone             = @saved_time_zone */ ;;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;;
/*!50003 SET character_set_client  = @saved_cs_client */ ;;
/*!50003 SET character_set_results = @saved_cs_results */ ;;
/*!50003 SET collation_connection  = @saved_col_connection */ ;;
DELIMITER ;
/*!50106 SET TIME_ZONE= @save_time_zone */ ;

--
-- Dumping routines for database 'reddit_parsing'
--
/*!50003 DROP PROCEDURE IF EXISTS `delete_rows_links` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `delete_rows_links`()
BEGIN 
	DELETE FROM SUBMISSION_COMMENT
    WHERE TIMESTAMPDIFF(HOUR, parsed_timestamp, now()) > 48;
    
	DELETE FROM submission
    WHERE TIMESTAMPDIFF(HOUR, parsed_timestamp, now()) > 48;
    
	DELETE FROM subreddit_active_users
    WHERE TIMESTAMPDIFF(HOUR, parsed_timestamp, now()) > 48;
    
	DELETE FROM subreddit
    WHERE TIMESTAMPDIFF(HOUR, parsed_timestamp, now()) > 48;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-06  0:29:09
