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
  `author` text COMMENT 'author of the submission',
  `upvotes` int DEFAULT NULL COMMENT 'possitive votes',
  `downvotes` int DEFAULT NULL COMMENT 'negative votes',
  `created_timestamp` datetime DEFAULT NULL COMMENT 'submission creation timestamp',
  `parsed_timestamp` datetime DEFAULT NULL COMMENT 'timestamp when submission was written to db. For compliance with Reddit api licence',
  PRIMARY KEY (`id`),
  UNIQUE KEY `url` (`url`),
  UNIQUE KEY `full_name` (`full_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `submission`
--

LOCK TABLES `submission` WRITE;
/*!40000 ALTER TABLE `submission` DISABLE KEYS */;
/*!40000 ALTER TABLE `submission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `submission_comment`
--

DROP TABLE IF EXISTS `submission_comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `submission_comment` (
  `id` int NOT NULL AUTO_INCREMENT,
  `full_name` varchar(768) NOT NULL COMMENT 'reddit-qualified full name',
  `submission_name` varchar(768) DEFAULT NULL COMMENT 'reddit-qualified full name',
  `title` text COMMENT 'author-provided title',
  `text_body` text COMMENT 'possibly empty string of text',
  `author` text COMMENT 'author of the submission',
  `upvotes` int DEFAULT NULL COMMENT 'possitive votes',
  `downvotes` int DEFAULT NULL COMMENT 'negative votes',
  `created_timestamp` datetime DEFAULT NULL COMMENT 'submission creation timestamp',
  `parsed_timestamp` datetime DEFAULT NULL COMMENT 'timestamp when comment was written to db. For compliance with Reddit api licence',
  PRIMARY KEY (`id`),
  UNIQUE KEY `full_name` (`full_name`),
  KEY `submission_name` (`submission_name`),
  CONSTRAINT `submission_comment_ibfk_1` FOREIGN KEY (`submission_name`) REFERENCES `submission` (`full_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `submission_comment`
--

LOCK TABLES `submission_comment` WRITE;
/*!40000 ALTER TABLE `submission_comment` DISABLE KEYS */;
/*!40000 ALTER TABLE `submission_comment` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-02-26 10:47:29
