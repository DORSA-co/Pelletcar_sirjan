-- MySQL dump 10.13  Distrib 8.0.23, for Win64 (x86_64)
--
-- Host: localhost    Database: dpis
-- ------------------------------------------------------
-- Server version	8.0.23

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
-- Table structure for table `general_setting`
--

DROP TABLE IF EXISTS `general_setting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `general_setting` (
  `id` int NOT NULL AUTO_INCREMENT,
  `plt_number_dis` int DEFAULT '45',
  `table_name` varchar(45) DEFAULT 'pallet',
  `database_name` varchar(45) DEFAULT 'PALLETCAR',
  `db_days_to_save` int DEFAULT '3',
  `ip` varchar(45) DEFAULT '169.254.116.245',
  `img_path` varchar(150) DEFAULT 'F:\\arshad\\folad projects\\pallet car\\sirjan project\\DPIS\\pics',
  `port` int DEFAULT '502',
  `timeout` int DEFAULT '50',
  `madule_path` varchar(150) DEFAULT 'F:\\arshad\\folad projects\\pallet car\\sirjan project\\DPIS\\sirjan run\\final\\Pallet-car-master\\Pallet-car-master\\main_func.py',
  `ip_speed` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `general_setting`
--

LOCK TABLES `general_setting` WRITE;
/*!40000 ALTER TABLE `general_setting` DISABLE KEYS */;
INSERT INTO `general_setting` VALUES (30,45,'pallet','PALLETCAR',3,'169.254.116.245','F:\\arshad\\folad projects\\pic\\palletcar\\pallect_proc_pic',502,50,'F:\\arshad\\folad projects\\pallet car\\sirjan project\\DPIS\\sirjan run\\final\\Pallet-car-master\\Pallet-car-master\\main_func.py',NULL),(31,45,'pallet','PALLETCAR',3,'169.254.116.245','F:\\arshad\\folad projects\\pic\\palletcar\\pallect_proc_pic',502,50,'F:\\arshad\\folad projects\\pallet car\\sirjan project\\DPIS\\sirjan run\\final\\Pallet-car-master\\Pallet-car-master\\main_func.py',NULL);
/*!40000 ALTER TABLE `general_setting` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-01-14 12:39:17
