-- MySQL dump 10.16  Distrib 10.1.21-MariaDB, for Linux (i686)
--
-- Host: localhost    Database: localhost
-- ------------------------------------------------------
-- Server version	10.1.21-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table classes
--

DROP TABLE IF EXISTS classes;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE classes (
  class_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  course_id INTEGER NOT NULL,
  course_date date DEFAULT NULL,
  instructor_id INTEGER NOT NULL,
  administrator_id INTEGER NOT NULL,
  fee_for_members decimal(10,2) DEFAULT NULL
);
-- ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table classes
--

-- LOCK TABLES classes WRITE;
/*!40000 ALTER TABLE classes DISABLE KEYS */;
/*!40000 ALTER TABLE classes ENABLE KEYS */;
-- UNLOCK TABLES;

--
-- Table structure for table courses
--

DROP TABLE IF EXISTS courses;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE courses (
  course_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  course_title varchar(30) DEFAULT NULL,
  course_syllabus blob
);
-- ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table courses
--

-- LOCK TABLES courses WRITE;
/*!40000 ALTER TABLE courses DISABLE KEYS */;
/*!40000 ALTER TABLE courses ENABLE KEYS */;
-- UNLOCK TABLES;

--
-- Table structure for table members
--

DROP TABLE IF EXISTS members;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE members (
  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  username varchar(60) DEFAULT NULL,
  lastname varchar(30) NOT NULL,
  firstname varchar(30) NOT NULL,
  photo blob,
  nickname varchar(30) DEFAULT NULL,
  mailing_address varchar(50) NOT NULL,
  city varchar(30) NOT NULL,
  province varchar(30) NOT NULL,
  postal_code varchar(8) DEFAULT NULL,
  email varchar(30) NOT NULL,
  phone varchar(20) DEFAULT NULL,
  emergency_contact varchar(30) DEFAULT NULL,
  emergency_contact_phone varchar(20) DEFAULT NULL,
  membership_class enum('full','student','friend') DEFAULT NULL,
  application_date date DEFAULT NULL,
  current_start date DEFAULT NULL,
  vetted date DEFAULT NULL,
  ended_date date DEFAULT NULL,
  earliest_membership_start date DEFAULT NULL,
  latest_membership_start date DEFAULT NULL,
  current_membership_start date DEFAULT NULL
);
-- ENGINE=InnoDB AUTOINCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table members
--

-- LOCK TABLES members WRITE;
/*!40000 ALTER TABLE members DISABLE KEYS */;
INSERT INTO members VALUES (1,'mike.morrow','Morrow','Mike','','','4632 Montalban Drive NW','Calgary','AB','T3B 1E4','morrow@morrow.pl','403-286-1331','','','full','2013-02-05','2013-02-05','2014-10-23','0000-00-00','2013-02-05','2013-02-05','2013-02-05');
/*!40000 ALTER TABLE members ENABLE KEYS */;
-- UNLOCK TABLES;

--
-- Table structure for table passwords
--

DROP TABLE IF EXISTS passwords;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE passwords (
  id INTEGER NOT NULL,
  password varchar(64) NOT NULL
);
-- ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table passwords
--

-- LOCK TABLES passwords WRITE;
/*!40000 ALTER TABLE passwords DISABLE KEYS */;
/*!40000 ALTER TABLE passwords ENABLE KEYS */;
-- UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-07-08 11:01:21
