-- MariaDB dump 10.19  Distrib 10.5.22-MariaDB, for Linux (x86_64)
--
-- Host: classmysql.engr.oregonstate.edu    Database: cs340_sanromau
-- ------------------------------------------------------
-- Server version	10.6.19-MariaDB-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Customer_Seller_Relationships`
--

DROP TABLE IF EXISTS `Customer_Seller_Relationships`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Customer_Seller_Relationships` (
  `csrID` int(11) NOT NULL AUTO_INCREMENT,
  `customerID` int(11) NOT NULL,
  `sellerID` int(11) NOT NULL,
  `email_opt_out` tinyint(1) DEFAULT 1,
  PRIMARY KEY (`csrID`),
  KEY `customerID` (`customerID`),
  KEY `sellerID` (`sellerID`),
  CONSTRAINT `Customer_Seller_Relationships_ibfk_1` FOREIGN KEY (`customerID`) REFERENCES `Customers` (`customerID`) ON DELETE CASCADE,
  CONSTRAINT `Customer_Seller_Relationships_ibfk_2` FOREIGN KEY (`sellerID`) REFERENCES `Sellers` (`sellerID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Customer_Seller_Relationships`
--

LOCK TABLES `Customer_Seller_Relationships` WRITE;
/*!40000 ALTER TABLE `Customer_Seller_Relationships` DISABLE KEYS */;
INSERT INTO `Customer_Seller_Relationships` VALUES (3,3,3,1);
/*!40000 ALTER TABLE `Customer_Seller_Relationships` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Customers`
--

DROP TABLE IF EXISTS `Customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Customers` (
  `customerID` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(32) NOT NULL,
  `last_name` varchar(32) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(32) NOT NULL,
  `phone_number` varchar(12) DEFAULT NULL,
  PRIMARY KEY (`customerID`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Customers`
--

LOCK TABLES `Customers` WRITE;
/*!40000 ALTER TABLE `Customers` DISABLE KEYS */;
INSERT INTO `Customers` VALUES (3,'John','King','jamesKing@omron.ai','2p0a2s4s?','334-758-8765'),(13,'Micheal','Scott','mscotty@gmail.com','345wam','433-567-9000'),(16,'Rod','San Roman','rodSaan@gmail.com','fbbs233314f','2104735555');
/*!40000 ALTER TABLE `Customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Line_Items`
--

DROP TABLE IF EXISTS `Line_Items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Line_Items` (
  `lineitemID` int(11) NOT NULL AUTO_INCREMENT,
  `orderID` int(11) NOT NULL,
  `productID` int(11) NOT NULL,
  `sell_price` decimal(6,2) NOT NULL,
  `qty` int(11) NOT NULL,
  PRIMARY KEY (`lineitemID`),
  UNIQUE KEY `orderID` (`orderID`,`productID`),
  KEY `productID` (`productID`),
  CONSTRAINT `Line_Items_ibfk_1` FOREIGN KEY (`orderID`) REFERENCES `Orders` (`orderID`) ON DELETE CASCADE,
  CONSTRAINT `Line_Items_ibfk_2` FOREIGN KEY (`productID`) REFERENCES `Products` (`productID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Line_Items`
--

LOCK TABLES `Line_Items` WRITE;
/*!40000 ALTER TABLE `Line_Items` DISABLE KEYS */;
INSERT INTO `Line_Items` VALUES (3,3,3,19.99,4);
/*!40000 ALTER TABLE `Line_Items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Orders`
--

DROP TABLE IF EXISTS `Orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Orders` (
  `orderID` int(11) NOT NULL AUTO_INCREMENT,
  `customerID` int(11) NOT NULL,
  `order_date` date NOT NULL,
  `shipped` tinyint(1) DEFAULT 0,
  `total` decimal(6,2) NOT NULL,
  PRIMARY KEY (`orderID`),
  KEY `customerID` (`customerID`),
  CONSTRAINT `Orders_ibfk_1` FOREIGN KEY (`customerID`) REFERENCES `Customers` (`customerID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Orders`
--

LOCK TABLES `Orders` WRITE;
/*!40000 ALTER TABLE `Orders` DISABLE KEYS */;
INSERT INTO `Orders` VALUES (3,3,'2021-10-01',1,86.36);
/*!40000 ALTER TABLE `Orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Products`
--

DROP TABLE IF EXISTS `Products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Products` (
  `productID` int(11) NOT NULL AUTO_INCREMENT,
  `sellerID` int(11) NOT NULL,
  `category` varchar(32) NOT NULL,
  `brand` varchar(32) DEFAULT NULL,
  `size` varchar(32) DEFAULT NULL,
  `price` decimal(6,2) NOT NULL,
  `product_condition` varchar(32) NOT NULL,
  `color` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`productID`),
  KEY `sellerID` (`sellerID`),
  CONSTRAINT `Products_ibfk_1` FOREIGN KEY (`sellerID`) REFERENCES `Sellers` (`sellerID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Products`
--

LOCK TABLES `Products` WRITE;
/*!40000 ALTER TABLE `Products` DISABLE KEYS */;
INSERT INTO `Products` VALUES (1,1,'Shirts','Adidas','Medium',119.99,'New','Black'),(2,2,'Pants','Nike','Large',49.99,'New','Red'),(3,3,'Pants','Arizona','Large',19.99,'Used','White'),(4,4,'Accessories','Eddie Bauer','Small',15.99,'Used','Blue');
/*!40000 ALTER TABLE `Products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Sellers`
--

DROP TABLE IF EXISTS `Sellers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Sellers` (
  `sellerID` int(11) NOT NULL AUTO_INCREMENT,
  `seller_first_name` varchar(32) NOT NULL,
  `seller_last_name` varchar(32) NOT NULL,
  `store_name` varchar(32) NOT NULL,
  `store_rating` decimal(3,1) DEFAULT NULL,
  `follower_count` int(11) DEFAULT NULL,
  PRIMARY KEY (`sellerID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Sellers`
--

LOCK TABLES `Sellers` WRITE;
/*!40000 ALTER TABLE `Sellers` DISABLE KEYS */;
INSERT INTO `Sellers` VALUES (1,'Pam','Brell','Winner Tech Shop',2.8,1023),(2,'Jon','Wimber','Wimber Wear',4.5,850),(3,'Ella','Garcia','Crate and Home',4.9,670),(4,'Sonny','Smith','Son Shades',3.7,1540);
/*!40000 ALTER TABLE `Sellers` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-24 20:28:15
