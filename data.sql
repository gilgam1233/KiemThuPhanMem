-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: hangydb
-- ------------------------------------------------------
-- Server version	9.4.0

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
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `name` varchar(50) NOT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  `is_active` tinyint(1) DEFAULT NULL,
  `created_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES ('Dụng cụ nhà bếp',1,1,'2026-04-11 01:03:32'),('Bát đĩa',2,1,'2026-04-11 01:03:32'),('Gia vị',3,1,'2026-04-11 01:03:32'),('Đồ gỗ',4,1,'2026-04-11 01:03:32'),('Inox',5,1,'2026-04-11 01:03:32');
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_details`
--

DROP TABLE IF EXISTS `order_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_details` (
  `order_id` int NOT NULL,
  `product_id` int NOT NULL,
  `created_date` datetime DEFAULT NULL,
  `quantity` int NOT NULL,
  `price` float NOT NULL,
  PRIMARY KEY (`order_id`,`product_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `order_details_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`),
  CONSTRAINT `order_details_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_details`
--

LOCK TABLES `order_details` WRITE;
/*!40000 ALTER TABLE `order_details` DISABLE KEYS */;
INSERT INTO `order_details` VALUES (1,32,'2026-04-11 01:03:32',1,275000),(2,53,'2026-04-11 01:03:32',3,495000),(3,32,'2026-04-11 01:03:32',3,275000),(4,15,'2026-04-11 01:03:32',3,975000),(4,39,'2026-04-11 01:03:32',2,925000),(5,20,'2026-04-11 01:03:32',2,975000),(5,29,'2026-04-11 01:03:32',3,865000),(5,60,'2026-04-11 01:03:32',1,710000),(6,6,'2026-04-11 01:03:32',3,770000),(6,10,'2026-04-11 01:03:32',1,865000),(6,37,'2026-04-11 01:03:32',3,295000),(6,64,'2026-04-11 01:03:32',2,210000),(7,3,'2026-04-11 01:03:32',2,485000),(7,46,'2026-04-11 01:03:32',2,60000),(7,71,'2026-04-11 01:03:32',3,495000),(7,79,'2026-04-11 01:03:32',2,180000),(8,14,'2026-04-11 01:03:32',3,90000),(9,100,'2026-04-11 01:03:32',3,960000),(10,1,'2026-04-11 01:03:32',1,385000),(10,17,'2026-04-11 01:03:32',1,265000),(10,18,'2026-04-11 01:03:32',2,480000),(10,61,'2026-04-11 01:03:32',1,735000),(11,26,'2026-04-11 01:03:32',1,340000),(11,52,'2026-04-11 01:03:32',1,475000),(11,56,'2026-04-11 01:03:32',1,965000),(11,85,'2026-04-11 01:03:32',1,460000),(12,6,'2026-04-11 01:03:32',2,770000),(12,86,'2026-04-11 01:03:32',2,555000),(13,12,'2026-04-11 01:03:32',2,905000),(13,19,'2026-04-11 01:03:32',2,550000),(13,44,'2026-04-11 01:03:32',3,955000),(13,86,'2026-04-11 01:03:32',1,555000),(14,8,'2026-04-11 01:03:32',3,875000),(15,17,'2026-04-11 01:03:32',3,265000),(15,31,'2026-04-11 01:03:32',1,745000),(15,72,'2026-04-11 01:03:32',3,995000),(16,17,'2026-04-11 01:03:32',3,265000),(16,54,'2026-04-11 01:03:32',2,865000),(16,81,'2026-04-11 01:03:32',1,335000),(17,1,'2026-04-11 01:03:32',1,385000),(17,65,'2026-04-11 01:03:32',3,480000),(17,98,'2026-04-11 01:03:32',2,985000),(18,14,'2026-04-11 01:03:32',3,90000),(18,57,'2026-04-11 01:03:32',3,525000),(18,94,'2026-04-11 01:03:32',3,485000),(19,27,'2026-04-11 01:03:32',2,730000),(19,93,'2026-04-11 01:03:32',2,455000),(20,4,'2026-04-11 01:03:32',3,665000),(20,34,'2026-04-11 01:03:32',3,530000),(20,94,'2026-04-11 01:03:32',1,485000),(20,98,'2026-04-11 01:03:32',1,985000),(21,2,'2026-04-14 15:22:26',1,95000),(22,3,'2026-04-14 15:51:11',1,485000),(22,4,'2026-04-14 15:51:11',1,665000);
/*!40000 ALTER TABLE `order_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `id` int NOT NULL AUTO_INCREMENT,
  `total_amount` float NOT NULL,
  `final_amount` float NOT NULL,
  `created_date` datetime DEFAULT NULL,
  `status` enum('PENDING','CONFIRMED','COMPLETED','CANCELED') DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (1,275000,251000,'2026-04-11 01:03:32','CONFIRMED',15),(2,1485000,1485000,'2026-04-11 01:03:32','PENDING',27),(3,825000,825000,'2026-04-11 01:03:32','PENDING',37),(4,4775000,4775000,'2026-04-11 01:03:32','COMPLETED',46),(5,5255000,5255000,'2026-04-11 01:03:32','PENDING',15),(6,4480000,4444000,'2026-04-11 01:03:32','CONFIRMED',27),(7,2935000,2935000,'2026-04-11 01:03:32','PENDING',10),(8,270000,210600,'2026-04-11 01:03:32','CANCELED',15),(9,2880000,2678400,'2026-04-11 01:03:32','COMPLETED',39),(10,2345000,2312000,'2026-04-11 01:03:32','CONFIRMED',26),(11,2240000,2240000,'2026-04-11 01:03:32','CONFIRMED',11),(12,2650000,1908000,'2026-04-11 01:03:32','PENDING',46),(13,6330000,6330000,'2026-04-11 01:03:32','CONFIRMED',17),(14,2625000,2563000,'2026-04-11 01:03:32','CONFIRMED',24),(15,4525000,4525000,'2026-04-11 01:03:32','CONFIRMED',9),(16,2860000,2860000,'2026-04-11 01:03:32','COMPLETED',28),(17,3795000,3795000,'2026-04-11 01:03:32','PENDING',22),(18,3300000,3280000,'2026-04-11 01:03:32','CONFIRMED',48),(19,2370000,2370000,'2026-04-11 01:03:32','PENDING',27),(20,5055000,5055000,'2026-04-11 01:03:32','CONFIRMED',20),(21,95000,95000,'2026-04-14 15:22:26','PENDING',2),(22,1150000,1150000,'2026-04-14 15:51:11','PENDING',51);
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `price` float NOT NULL,
  `image` varchar(255) DEFAULT NULL,
  `category_id` int DEFAULT NULL,
  `created_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `products_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,'Bát sứ cao cấp số 0',385000,'cloudinary_link',4,'2026-04-11 01:03:32'),(2,'Thìa gỗ cao cấp số 1',95000,'cloudinary_link',3,'2026-04-11 01:03:32'),(3,'Hũ gia vị cao cấp số 2',485000,'cloudinary_link',5,'2026-04-11 01:03:32'),(4,'Muôi inox cao cấp số 3',665000,'cloudinary_link',2,'2026-04-11 01:03:32'),(5,'Chảo gang cao cấp số 4',825000,'cloudinary_link',5,'2026-04-11 01:03:32'),(6,'Bát sứ cao cấp số 5',770000,'cloudinary_link',3,'2026-04-11 01:03:32'),(7,'Thìa gỗ cao cấp số 6',65000,'cloudinary_link',4,'2026-04-11 01:03:32'),(8,'Hũ gia vị cao cấp số 7',875000,'cloudinary_link',5,'2026-04-11 01:03:32'),(9,'Muôi inox cao cấp số 8',605000,'cloudinary_link',5,'2026-04-11 01:03:32'),(10,'Chảo gang cao cấp số 9',865000,'cloudinary_link',5,'2026-04-11 01:03:32'),(11,'Bát sứ cao cấp số 10',670000,'cloudinary_link',5,'2026-04-11 01:03:32'),(12,'Thìa gỗ cao cấp số 11',905000,'cloudinary_link',4,'2026-04-11 01:03:32'),(13,'Hũ gia vị cao cấp số 12',525000,'cloudinary_link',5,'2026-04-11 01:03:32'),(14,'Muôi inox cao cấp số 13',90000,'cloudinary_link',2,'2026-04-11 01:03:32'),(15,'Chảo gang cao cấp số 14',975000,'cloudinary_link',1,'2026-04-11 01:03:32'),(16,'Bát sứ cao cấp số 15',670000,'cloudinary_link',3,'2026-04-11 01:03:32'),(17,'Thìa gỗ cao cấp số 16',265000,'cloudinary_link',3,'2026-04-11 01:03:32'),(18,'Hũ gia vị cao cấp số 17',480000,'cloudinary_link',5,'2026-04-11 01:03:32'),(19,'Muôi inox cao cấp số 18',550000,'cloudinary_link',1,'2026-04-11 01:03:32'),(20,'Chảo gang cao cấp số 19',975000,'cloudinary_link',4,'2026-04-11 01:03:32'),(21,'Bát sứ cao cấp số 20',545000,'cloudinary_link',5,'2026-04-11 01:03:32'),(22,'Thìa gỗ cao cấp số 21',480000,'cloudinary_link',1,'2026-04-11 01:03:32'),(23,'Hũ gia vị cao cấp số 22',290000,'cloudinary_link',5,'2026-04-11 01:03:32'),(24,'Muôi inox cao cấp số 23',160000,'cloudinary_link',3,'2026-04-11 01:03:32'),(25,'Chảo gang cao cấp số 24',65000,'cloudinary_link',3,'2026-04-11 01:03:32'),(26,'Bát sứ cao cấp số 25',340000,'cloudinary_link',4,'2026-04-11 01:03:32'),(27,'Thìa gỗ cao cấp số 26',730000,'cloudinary_link',5,'2026-04-11 01:03:32'),(28,'Hũ gia vị cao cấp số 27',975000,'cloudinary_link',1,'2026-04-11 01:03:32'),(29,'Muôi inox cao cấp số 28',865000,'cloudinary_link',3,'2026-04-11 01:03:32'),(30,'Chảo gang cao cấp số 29',680000,'cloudinary_link',2,'2026-04-11 01:03:32'),(31,'Bát sứ cao cấp số 30',745000,'cloudinary_link',4,'2026-04-11 01:03:32'),(32,'Thìa gỗ cao cấp số 31',275000,'cloudinary_link',2,'2026-04-11 01:03:32'),(33,'Hũ gia vị cao cấp số 32',735000,'cloudinary_link',4,'2026-04-11 01:03:32'),(34,'Muôi inox cao cấp số 33',530000,'cloudinary_link',4,'2026-04-11 01:03:32'),(35,'Chảo gang cao cấp số 34',105000,'cloudinary_link',1,'2026-04-11 01:03:32'),(36,'Bát sứ cao cấp số 35',220000,'cloudinary_link',4,'2026-04-11 01:03:32'),(37,'Thìa gỗ cao cấp số 36',295000,'cloudinary_link',1,'2026-04-11 01:03:32'),(38,'Hũ gia vị cao cấp số 37',375000,'cloudinary_link',3,'2026-04-11 01:03:32'),(39,'Muôi inox cao cấp số 38',925000,'cloudinary_link',3,'2026-04-11 01:03:32'),(40,'Chảo gang cao cấp số 39',605000,'cloudinary_link',4,'2026-04-11 01:03:32'),(41,'Bát sứ cao cấp số 40',50000,'cloudinary_link',1,'2026-04-11 01:03:32'),(42,'Thìa gỗ cao cấp số 41',840000,'cloudinary_link',1,'2026-04-11 01:03:32'),(43,'Hũ gia vị cao cấp số 42',700000,'cloudinary_link',3,'2026-04-11 01:03:32'),(44,'Muôi inox cao cấp số 43',955000,'cloudinary_link',1,'2026-04-11 01:03:32'),(45,'Chảo gang cao cấp số 44',155000,'cloudinary_link',4,'2026-04-11 01:03:32'),(46,'Bát sứ cao cấp số 45',60000,'cloudinary_link',5,'2026-04-11 01:03:32'),(47,'Thìa gỗ cao cấp số 46',530000,'cloudinary_link',1,'2026-04-11 01:03:32'),(48,'Hũ gia vị cao cấp số 47',745000,'cloudinary_link',4,'2026-04-11 01:03:32'),(49,'Muôi inox cao cấp số 48',85000,'cloudinary_link',3,'2026-04-11 01:03:32'),(50,'Chảo gang cao cấp số 49',385000,'cloudinary_link',4,'2026-04-11 01:03:32'),(51,'Bát sứ cao cấp số 50',90000,'cloudinary_link',5,'2026-04-11 01:03:32'),(52,'Thìa gỗ cao cấp số 51',475000,'cloudinary_link',4,'2026-04-11 01:03:32'),(53,'Hũ gia vị cao cấp số 52',495000,'cloudinary_link',1,'2026-04-11 01:03:32'),(54,'Muôi inox cao cấp số 53',865000,'cloudinary_link',2,'2026-04-11 01:03:32'),(55,'Chảo gang cao cấp số 54',585000,'cloudinary_link',1,'2026-04-11 01:03:32'),(56,'Bát sứ cao cấp số 55',965000,'cloudinary_link',2,'2026-04-11 01:03:32'),(57,'Thìa gỗ cao cấp số 56',525000,'cloudinary_link',2,'2026-04-11 01:03:32'),(58,'Hũ gia vị cao cấp số 57',1000000,'cloudinary_link',1,'2026-04-11 01:03:32'),(59,'Muôi inox cao cấp số 58',850000,'cloudinary_link',1,'2026-04-11 01:03:32'),(60,'Chảo gang cao cấp số 59',710000,'cloudinary_link',4,'2026-04-11 01:03:32'),(61,'Bát sứ cao cấp số 60',735000,'cloudinary_link',3,'2026-04-11 01:03:32'),(62,'Thìa gỗ cao cấp số 61',235000,'cloudinary_link',3,'2026-04-11 01:03:32'),(63,'Hũ gia vị cao cấp số 62',545000,'cloudinary_link',3,'2026-04-11 01:03:32'),(64,'Muôi inox cao cấp số 63',210000,'cloudinary_link',5,'2026-04-11 01:03:32'),(65,'Chảo gang cao cấp số 64',480000,'cloudinary_link',5,'2026-04-11 01:03:32'),(66,'Bát sứ cao cấp số 65',200000,'cloudinary_link',2,'2026-04-11 01:03:32'),(67,'Thìa gỗ cao cấp số 66',800000,'cloudinary_link',4,'2026-04-11 01:03:32'),(68,'Hũ gia vị cao cấp số 67',600000,'cloudinary_link',1,'2026-04-11 01:03:32'),(69,'Muôi inox cao cấp số 68',995000,'cloudinary_link',2,'2026-04-11 01:03:32'),(70,'Chảo gang cao cấp số 69',630000,'cloudinary_link',1,'2026-04-11 01:03:32'),(71,'Bát sứ cao cấp số 70',495000,'cloudinary_link',4,'2026-04-11 01:03:32'),(72,'Thìa gỗ cao cấp số 71',995000,'cloudinary_link',4,'2026-04-11 01:03:32'),(73,'Hũ gia vị cao cấp số 72',435000,'cloudinary_link',4,'2026-04-11 01:03:32'),(74,'Muôi inox cao cấp số 73',85000,'cloudinary_link',2,'2026-04-11 01:03:32'),(75,'Chảo gang cao cấp số 74',715000,'cloudinary_link',3,'2026-04-11 01:03:32'),(76,'Bát sứ cao cấp số 75',710000,'cloudinary_link',5,'2026-04-11 01:03:32'),(77,'Thìa gỗ cao cấp số 76',760000,'cloudinary_link',2,'2026-04-11 01:03:32'),(78,'Hũ gia vị cao cấp số 77',485000,'cloudinary_link',5,'2026-04-11 01:03:32'),(79,'Muôi inox cao cấp số 78',180000,'cloudinary_link',5,'2026-04-11 01:03:32'),(80,'Chảo gang cao cấp số 79',975000,'cloudinary_link',3,'2026-04-11 01:03:32'),(81,'Bát sứ cao cấp số 80',335000,'cloudinary_link',5,'2026-04-11 01:03:32'),(82,'Thìa gỗ cao cấp số 81',485000,'cloudinary_link',1,'2026-04-11 01:03:32'),(83,'Hũ gia vị cao cấp số 82',395000,'cloudinary_link',5,'2026-04-11 01:03:32'),(84,'Muôi inox cao cấp số 83',360000,'cloudinary_link',2,'2026-04-11 01:03:32'),(85,'Chảo gang cao cấp số 84',460000,'cloudinary_link',3,'2026-04-11 01:03:32'),(86,'Bát sứ cao cấp số 85',555000,'cloudinary_link',1,'2026-04-11 01:03:32'),(87,'Thìa gỗ cao cấp số 86',690000,'cloudinary_link',1,'2026-04-11 01:03:32'),(88,'Hũ gia vị cao cấp số 87',300000,'cloudinary_link',5,'2026-04-11 01:03:32'),(89,'Muôi inox cao cấp số 88',305000,'cloudinary_link',1,'2026-04-11 01:03:32'),(90,'Chảo gang cao cấp số 89',295000,'cloudinary_link',3,'2026-04-11 01:03:32'),(91,'Bát sứ cao cấp số 90',770000,'cloudinary_link',2,'2026-04-11 01:03:32'),(92,'Thìa gỗ cao cấp số 91',155000,'cloudinary_link',5,'2026-04-11 01:03:32'),(93,'Hũ gia vị cao cấp số 92',455000,'cloudinary_link',1,'2026-04-11 01:03:32'),(94,'Muôi inox cao cấp số 93',485000,'cloudinary_link',5,'2026-04-11 01:03:32'),(95,'Chảo gang cao cấp số 94',735000,'cloudinary_link',2,'2026-04-11 01:03:32'),(96,'Bát sứ cao cấp số 95',730000,'cloudinary_link',2,'2026-04-11 01:03:32'),(97,'Thìa gỗ cao cấp số 96',665000,'cloudinary_link',4,'2026-04-11 01:03:32'),(98,'Hũ gia vị cao cấp số 97',985000,'cloudinary_link',4,'2026-04-11 01:03:32'),(99,'Muôi inox cao cấp số 98',85000,'cloudinary_link',3,'2026-04-11 01:03:32'),(100,'Chảo gang cao cấp số 99',960000,'cloudinary_link',5,'2026-04-11 01:03:32');
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `username` varchar(30) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('ADMIN','USER') DEFAULT NULL,
  `first_name` varchar(30) DEFAULT NULL,
  `last_name` varchar(30) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `avatar` varchar(255) DEFAULT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  `is_active` tinyint(1) DEFAULT NULL,
  `created_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('admin','202cb962ac59075b964b07152d234b70','ADMIN','Quản','Trị','admin@hangy.vn',NULL,'Trụ sở chính Hangy','cloudinary_link',1,1,'2026-04-11 01:03:32'),('user_0','202cb962ac59075b964b07152d234b70','USER','John','Vũ','user0@example.com','+84 64 1068855','585 John Đường\nJohnXã, 495936','cloudinary_link',2,1,'2026-04-11 01:03:32'),('user_1','202cb962ac59075b964b07152d234b70','USER','John','Nguyễn','user1@example.com','07 1012 2046','04 Mai Dãy\nHuyện JohnThị xã, 906647','cloudinary_link',3,1,'2026-04-11 01:03:32'),('user_2','202cb962ac59075b964b07152d234b70','USER','Jane','Mai','user2@example.com','+84-97-865 8021','558 Trần Dãy\nJaneThành phố, 298245','cloudinary_link',4,1,'2026-04-11 01:03:32'),('user_3','202cb962ac59075b964b07152d234b70','USER','John','Đặng','user3@example.com','+84 53 6880473','876 Nguyễn Đường\nThị xã JohnThành phố, 368815','cloudinary_link',5,1,'2026-04-11 01:03:32'),('user_4','202cb962ac59075b964b07152d234b70','USER','Jane','Vũ','user4@example.com','06 0191851','6 Jane Đường\nJaneThị xã, 134635','cloudinary_link',6,1,'2026-04-11 01:03:32'),('user_5','202cb962ac59075b964b07152d234b70','USER','Jane','Bùi','user5@example.com','00 2612 5310','4 Jane Số\nJohnXã, 454129','cloudinary_link',7,1,'2026-04-11 01:03:32'),('user_6','202cb962ac59075b964b07152d234b70','USER','John','Lê','user6@example.com','(09)660-2705','60 Jane Hẻm\nJohnXã, 861608','cloudinary_link',8,1,'2026-04-11 01:03:32'),('user_7','202cb962ac59075b964b07152d234b70','USER','Jane','Phạm','user7@example.com','+84-51-483354','830 Jane Làng\nHuyện JohnHuyện, 681471','cloudinary_link',9,1,'2026-04-11 01:03:32'),('user_8','202cb962ac59075b964b07152d234b70','USER','John','Mai','user8@example.com','(07) 7604 9756','0 Đặng Ngõ\nHuyện JaneHuyện, 801442','cloudinary_link',10,1,'2026-04-11 01:03:32'),('user_9','202cb962ac59075b964b07152d234b70','USER','Jane','Đặng','user9@example.com','03 7532 6066','6 Trần Khu\nHuyện JaneThành phố, 499072','cloudinary_link',11,1,'2026-04-11 01:03:32'),('user_10','202cb962ac59075b964b07152d234b70','USER','John','Hoàng','user10@example.com','04 1795374','789 Đặng Đường\nThành phố JohnThị xã, 792274','cloudinary_link',12,1,'2026-04-11 01:03:32'),('user_11','202cb962ac59075b964b07152d234b70','USER','Jane','Lê','user11@example.com','08 0782553','89 Hoàng Đường\nJaneQuận, 821409','cloudinary_link',13,1,'2026-04-11 01:03:32'),('user_12','202cb962ac59075b964b07152d234b70','USER','John','Vũ','user12@example.com','02 6560 9072','2 Jane Dãy\nJohnHuyện, 653449','cloudinary_link',14,1,'2026-04-11 01:03:32'),('user_13','202cb962ac59075b964b07152d234b70','USER','John','Trần','user13@example.com','09 8843816','096 Mai Tổ\nThị xã JohnQuận, 321910','cloudinary_link',15,1,'2026-04-11 01:03:32'),('user_14','202cb962ac59075b964b07152d234b70','USER','John','Nguyễn','user14@example.com','(03) 1600 6580','6 Lê Khu\nHuyện JaneQuận, 640535','cloudinary_link',16,1,'2026-04-11 01:03:32'),('user_15','202cb962ac59075b964b07152d234b70','USER','John','Đặng','user15@example.com','(02)736-3866','704 Jane Ngõ\nThành phố JaneHuyện, 678604','cloudinary_link',17,1,'2026-04-11 01:03:32'),('user_16','202cb962ac59075b964b07152d234b70','USER','John','Dương','user16@example.com','+84-54-536018','5 John Số\nThị xã JohnThị xã, 247400','cloudinary_link',18,1,'2026-04-11 01:03:32'),('user_17','202cb962ac59075b964b07152d234b70','USER','John','Lê','user17@example.com','(01)501-2376','021 Trần Hẻm\nHuyện JaneQuận, 956589','cloudinary_link',19,1,'2026-04-11 01:03:32'),('user_18','202cb962ac59075b964b07152d234b70','USER','John','Phạm','user18@example.com','(06)521-0456','081 John Khu\nQuận JohnXã, 904698','cloudinary_link',20,1,'2026-04-11 01:03:32'),('user_19','202cb962ac59075b964b07152d234b70','USER','Jane','Bùi','user19@example.com','+84-55-260945','80 Trần Số\nHuyện JaneThành phố, 869059','cloudinary_link',21,1,'2026-04-11 01:03:32'),('user_20','202cb962ac59075b964b07152d234b70','USER','John','Bùi','user20@example.com','+84-13-356 7488','02 Jane Hẻm\nQuận JohnHuyện, 227145','cloudinary_link',22,1,'2026-04-11 01:03:32'),('user_21','202cb962ac59075b964b07152d234b70','USER','John','Đặng','user21@example.com','+84 45 2461948','8 Jane Khu\nJaneQuận, 105610','cloudinary_link',23,1,'2026-04-11 01:03:32'),('user_22','202cb962ac59075b964b07152d234b70','USER','John','Trần','user22@example.com','+84-17-652260','621 Jane Số\nThị xã JaneThành phố, 124984','cloudinary_link',24,1,'2026-04-11 01:03:32'),('user_23','202cb962ac59075b964b07152d234b70','USER','John','Hoàng','user23@example.com','04 9083449','244 Jane Làng\nJohnThị xã, 168851','cloudinary_link',25,1,'2026-04-11 01:03:32'),('user_24','202cb962ac59075b964b07152d234b70','USER','John','Lê','user24@example.com','+84-08-317 9369','8 Trần Làng\nThị xã JohnXã, 426588','cloudinary_link',26,1,'2026-04-11 01:03:32'),('user_25','202cb962ac59075b964b07152d234b70','USER','John','Phạm','user25@example.com','+84-02-810 6796','6 Trần Ngõ\nQuận JohnPhường, 941895','cloudinary_link',27,1,'2026-04-11 01:03:32'),('user_26','202cb962ac59075b964b07152d234b70','USER','John','Hoàng','user26@example.com','05 8644 6288','992 Jane Làng\nJohnHuyện, 410649','cloudinary_link',28,1,'2026-04-11 01:03:32'),('user_27','202cb962ac59075b964b07152d234b70','USER','Jane','Đặng','user27@example.com','+84-48-995 3205','56 John Ngõ\nThị xã JohnXã, 812644','cloudinary_link',29,1,'2026-04-11 01:03:32'),('user_28','202cb962ac59075b964b07152d234b70','USER','John','Dương','user28@example.com','+84-38-755964','310 Jane Đường\nQuận JohnPhường, 819209','cloudinary_link',30,1,'2026-04-11 01:03:32'),('user_29','202cb962ac59075b964b07152d234b70','USER','Jane','Lê','user29@example.com','(08)382-7807','8 Phạm Ngõ\nJaneThị xã, 434055','cloudinary_link',31,1,'2026-04-11 01:03:32'),('user_30','202cb962ac59075b964b07152d234b70','USER','John','Bùi','user30@example.com','(06)157-7010','53 Hoàng Tổ\nThành phố JohnQuận, 785109','cloudinary_link',32,1,'2026-04-11 01:03:32'),('user_31','202cb962ac59075b964b07152d234b70','USER','Jane','Phạm','user31@example.com','(07)605-2458','30 John Đường\nJaneThị xã, 838485','cloudinary_link',33,1,'2026-04-11 01:03:32'),('user_32','202cb962ac59075b964b07152d234b70','USER','Jane','Trần','user32@example.com','(03)253-5671','6 John Khu\nThành phố JaneQuận, 299251','cloudinary_link',34,1,'2026-04-11 01:03:32'),('user_33','202cb962ac59075b964b07152d234b70','USER','John','Trần','user33@example.com','07 6706014','55 Trần Tổ\nThành phố JohnThị xã, 510869','cloudinary_link',35,1,'2026-04-11 01:03:32'),('user_34','202cb962ac59075b964b07152d234b70','USER','Jane','Nguyễn','user34@example.com','(03)454-2597','7 John Tổ\nThị xã JohnHuyện, 914283','cloudinary_link',36,1,'2026-04-11 01:03:32'),('user_35','202cb962ac59075b964b07152d234b70','USER','John','Phạm','user35@example.com','07 5777464','19 Bùi Hẻm\nThành phố JohnPhường, 536461','cloudinary_link',37,1,'2026-04-11 01:03:32'),('user_36','202cb962ac59075b964b07152d234b70','USER','Jane','Hoàng','user36@example.com','09 3428 3619','72 Jane Hẻm\nHuyện JaneQuận, 268096','cloudinary_link',38,1,'2026-04-11 01:03:32'),('user_37','202cb962ac59075b964b07152d234b70','USER','Jane','Vũ','user37@example.com','+84-39-343990','970 John Tổ\nHuyện JohnThành phố, 355198','cloudinary_link',39,1,'2026-04-11 01:03:32'),('user_38','202cb962ac59075b964b07152d234b70','USER','John','Đặng','user38@example.com','(01) 2762 1880','1 Lê Làng\nJohnThị xã, 901986','cloudinary_link',40,1,'2026-04-11 01:03:32'),('user_39','202cb962ac59075b964b07152d234b70','USER','John','Hoàng','user39@example.com','06 0974 6692','347 John Hẻm\nQuận JanePhường, 224468','cloudinary_link',41,1,'2026-04-11 01:03:32'),('user_40','202cb962ac59075b964b07152d234b70','USER','John','Vũ','user40@example.com','+84-20-763 8396','48 Vũ Làng\nQuận JohnThành phố, 792239','cloudinary_link',42,1,'2026-04-11 01:03:32'),('user_41','202cb962ac59075b964b07152d234b70','USER','John','Bùi','user41@example.com','+84-47-127581','702 Đặng Hẻm\nJaneHuyện, 222007','cloudinary_link',43,1,'2026-04-11 01:03:32'),('user_42','202cb962ac59075b964b07152d234b70','USER','Jane','Dương','user42@example.com','05 1354 4981','77 Lê Hẻm\nQuận JaneQuận, 856156','cloudinary_link',44,1,'2026-04-11 01:03:32'),('user_43','202cb962ac59075b964b07152d234b70','USER','Jane','Lê','user43@example.com','(08)365-6249','6 John Dãy\nQuận JohnXã, 460592','cloudinary_link',45,1,'2026-04-11 01:03:32'),('user_44','202cb962ac59075b964b07152d234b70','USER','Jane','Hoàng','user44@example.com','00 7570 3042','22 John Hẻm\nJaneXã, 597457','cloudinary_link',46,1,'2026-04-11 01:03:32'),('user_45','202cb962ac59075b964b07152d234b70','USER','John','Bùi','user45@example.com','+84-64-521374','647 Hoàng Đường\nQuận JohnThị xã, 905796','cloudinary_link',47,1,'2026-04-11 01:03:32'),('user_46','202cb962ac59075b964b07152d234b70','USER','Jane','Phạm','user46@example.com','+84 87 0995233','888 Mai Dãy\nJohnHuyện, 939533','cloudinary_link',48,1,'2026-04-11 01:03:32'),('user_47','202cb962ac59075b964b07152d234b70','USER','Jane','Phạm','user47@example.com','+84-93-308344','865 John Hẻm\nHuyện JohnHuyện, 211522','cloudinary_link',49,1,'2026-04-11 01:03:32'),('user_48','202cb962ac59075b964b07152d234b70','USER','Jane','Nguyễn','user48@example.com','+84-05-990 9651','63 Hoàng Khu\nHuyện JaneThị xã, 711859','cloudinary_link',50,1,'2026-04-11 01:03:32'),('hao','202cb962ac59075b964b07152d234b70','USER','Nguyễn','Hào','2351050039hao@ou.edu.vn','0566552355','Hóc Môn','cloudinary_link',51,1,'2026-04-11 01:04:09'),('ddd','202cb962ac59075b964b07152d234b70','USER','Nguyễn','Hào','2351050039ho@ou.edu.vn','0566552355','Hóc Môn','cloudinary_link',52,1,'2026-04-14 15:09:23'),('Hao2','202cb962ac59075b964b07152d234b70','USER','Nguyễn','Hào','235100039hao@ou.edu.vn','0566552355','Hóc Môn','https://res.cloudinary.com/dvvvepfpu/image/upload/v1776164331/hangy/xhzqxqjcxceapy3bbpra.jpg',53,1,'2026-04-14 17:59:03');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_vouchers`
--

DROP TABLE IF EXISTS `users_vouchers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_vouchers` (
  `user_id` int NOT NULL,
  `voucher_id` int NOT NULL,
  `order_id` int DEFAULT NULL,
  `is_used` tinyint(1) DEFAULT NULL,
  `used_date` datetime DEFAULT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  `is_active` tinyint(1) DEFAULT NULL,
  `created_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_id` (`order_id`),
  KEY `user_id` (`user_id`),
  KEY `voucher_id` (`voucher_id`),
  CONSTRAINT `users_vouchers_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `users_vouchers_ibfk_2` FOREIGN KEY (`voucher_id`) REFERENCES `vouchers` (`id`),
  CONSTRAINT `users_vouchers_ibfk_3` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_vouchers`
--

LOCK TABLES `users_vouchers` WRITE;
/*!40000 ALTER TABLE `users_vouchers` DISABLE KEYS */;
INSERT INTO `users_vouchers` VALUES (2,11,NULL,0,NULL,1,1,'2026-04-11 01:03:32'),(2,13,NULL,0,NULL,2,1,'2026-04-11 01:03:32'),(3,17,NULL,0,NULL,3,1,'2026-04-11 01:03:32'),(4,20,NULL,0,NULL,4,1,'2026-04-11 01:03:32'),(5,1,NULL,0,NULL,5,1,'2026-04-11 01:03:32'),(5,16,NULL,0,NULL,6,1,'2026-04-11 01:03:32'),(5,11,NULL,0,NULL,7,1,'2026-04-11 01:03:32'),(6,19,NULL,0,NULL,8,1,'2026-04-11 01:03:32'),(6,4,NULL,0,NULL,9,1,'2026-04-11 01:03:32'),(6,2,NULL,0,NULL,10,1,'2026-04-11 01:03:32'),(7,15,NULL,0,NULL,11,1,'2026-04-11 01:03:32'),(7,12,NULL,0,NULL,12,1,'2026-04-11 01:03:32'),(8,14,NULL,0,NULL,13,1,'2026-04-11 01:03:32'),(8,11,NULL,0,NULL,14,1,'2026-04-11 01:03:32'),(8,12,NULL,0,NULL,15,1,'2026-04-11 01:03:32'),(9,15,NULL,0,NULL,16,1,'2026-04-11 01:03:32'),(10,7,NULL,0,NULL,17,1,'2026-04-11 01:03:32'),(10,6,NULL,0,NULL,18,1,'2026-04-11 01:03:32'),(11,2,NULL,0,NULL,19,1,'2026-04-11 01:03:32'),(11,14,NULL,0,NULL,20,1,'2026-04-11 01:03:32'),(12,17,NULL,0,NULL,21,1,'2026-04-11 01:03:32'),(12,9,NULL,0,NULL,22,1,'2026-04-11 01:03:32'),(13,18,NULL,0,NULL,23,1,'2026-04-11 01:03:32'),(14,12,NULL,0,NULL,24,1,'2026-04-11 01:03:32'),(14,3,NULL,0,NULL,25,1,'2026-04-11 01:03:32'),(15,4,1,1,'2026-04-11 01:03:32',26,1,'2026-04-11 01:03:32'),(15,9,8,1,'2026-04-11 01:03:32',27,1,'2026-04-11 01:03:32'),(16,20,NULL,0,NULL,28,1,'2026-04-11 01:03:32'),(16,11,NULL,0,NULL,29,1,'2026-04-11 01:03:32'),(16,2,NULL,0,NULL,30,1,'2026-04-11 01:03:32'),(17,2,NULL,0,NULL,31,1,'2026-04-11 01:03:32'),(17,19,NULL,0,NULL,32,1,'2026-04-11 01:03:32'),(18,10,NULL,0,NULL,33,1,'2026-04-11 01:03:32'),(18,4,NULL,0,NULL,34,1,'2026-04-11 01:03:32'),(19,19,NULL,0,NULL,35,1,'2026-04-11 01:03:32'),(19,11,NULL,0,NULL,36,1,'2026-04-11 01:03:32'),(20,15,NULL,0,NULL,37,1,'2026-04-11 01:03:32'),(21,15,NULL,0,NULL,38,1,'2026-04-11 01:03:32'),(21,19,NULL,0,NULL,39,1,'2026-04-11 01:03:32'),(22,12,NULL,0,NULL,40,1,'2026-04-11 01:03:32'),(22,8,NULL,0,NULL,41,1,'2026-04-11 01:03:32'),(22,15,NULL,0,NULL,42,1,'2026-04-11 01:03:32'),(23,19,NULL,0,NULL,43,1,'2026-04-11 01:03:32'),(23,9,NULL,0,NULL,44,1,'2026-04-11 01:03:32'),(23,11,NULL,0,NULL,45,1,'2026-04-11 01:03:32'),(24,6,14,1,'2026-04-11 01:03:32',46,1,'2026-04-11 01:03:32'),(25,1,NULL,0,NULL,47,1,'2026-04-11 01:03:32'),(26,16,10,1,'2026-04-11 01:03:32',48,1,'2026-04-11 01:03:32'),(26,5,NULL,0,NULL,49,1,'2026-04-11 01:03:32'),(27,18,6,1,'2026-04-11 01:03:32',50,1,'2026-04-11 01:03:32'),(27,2,NULL,0,NULL,51,1,'2026-04-11 01:03:32'),(28,18,NULL,0,NULL,52,1,'2026-04-11 01:03:32'),(28,5,NULL,0,NULL,53,1,'2026-04-11 01:03:32'),(29,12,NULL,0,NULL,54,1,'2026-04-11 01:03:32'),(29,8,NULL,0,NULL,55,1,'2026-04-11 01:03:32'),(30,2,NULL,0,NULL,56,1,'2026-04-11 01:03:32'),(30,15,NULL,0,NULL,57,1,'2026-04-11 01:03:32'),(30,17,NULL,0,NULL,58,1,'2026-04-11 01:03:32'),(31,10,NULL,0,NULL,59,1,'2026-04-11 01:03:32'),(31,19,NULL,0,NULL,60,1,'2026-04-11 01:03:32'),(31,1,NULL,0,NULL,61,1,'2026-04-11 01:03:32'),(32,13,NULL,0,NULL,62,1,'2026-04-11 01:03:32'),(32,8,NULL,0,NULL,63,1,'2026-04-11 01:03:32'),(33,3,NULL,0,NULL,64,1,'2026-04-11 01:03:32'),(33,9,NULL,0,NULL,65,1,'2026-04-11 01:03:32'),(33,10,NULL,0,NULL,66,1,'2026-04-11 01:03:32'),(34,14,NULL,0,NULL,67,1,'2026-04-11 01:03:32'),(35,14,NULL,0,NULL,68,1,'2026-04-11 01:03:32'),(35,2,NULL,0,NULL,69,1,'2026-04-11 01:03:32'),(36,1,NULL,0,NULL,70,1,'2026-04-11 01:03:32'),(36,16,NULL,0,NULL,71,1,'2026-04-11 01:03:32'),(36,6,NULL,0,NULL,72,1,'2026-04-11 01:03:32'),(37,2,NULL,0,NULL,73,1,'2026-04-11 01:03:32'),(38,17,NULL,0,NULL,74,1,'2026-04-11 01:03:32'),(38,6,NULL,0,NULL,75,1,'2026-04-11 01:03:32'),(39,17,9,1,'2026-04-11 01:03:32',76,1,'2026-04-11 01:03:32'),(39,7,NULL,0,NULL,77,1,'2026-04-11 01:03:32'),(39,10,NULL,0,NULL,78,1,'2026-04-11 01:03:32'),(40,15,NULL,0,NULL,79,1,'2026-04-11 01:03:32'),(40,8,NULL,0,NULL,80,1,'2026-04-11 01:03:32'),(41,17,NULL,0,NULL,81,1,'2026-04-11 01:03:32'),(41,3,NULL,0,NULL,82,1,'2026-04-11 01:03:32'),(42,15,NULL,0,NULL,83,1,'2026-04-11 01:03:32'),(43,18,NULL,0,NULL,84,1,'2026-04-11 01:03:32'),(43,20,NULL,0,NULL,85,1,'2026-04-11 01:03:32'),(43,9,NULL,0,NULL,86,1,'2026-04-11 01:03:32'),(44,17,NULL,0,NULL,87,1,'2026-04-11 01:03:32'),(45,13,NULL,0,NULL,88,1,'2026-04-11 01:03:32'),(46,15,12,1,'2026-04-11 01:03:32',89,1,'2026-04-11 01:03:32'),(46,4,NULL,0,NULL,90,1,'2026-04-11 01:03:32'),(47,19,NULL,0,NULL,91,1,'2026-04-11 01:03:32'),(48,14,18,1,'2026-04-11 01:03:32',92,1,'2026-04-11 01:03:32'),(48,17,NULL,0,NULL,93,1,'2026-04-11 01:03:32'),(49,5,NULL,0,NULL,94,1,'2026-04-11 01:03:32'),(49,16,NULL,0,NULL,95,1,'2026-04-11 01:03:32'),(50,7,NULL,0,NULL,96,1,'2026-04-11 01:03:32');
/*!40000 ALTER TABLE `users_vouchers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vouchers`
--

DROP TABLE IF EXISTS `vouchers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vouchers` (
  `code` varchar(50) NOT NULL,
  `discount_type` enum('PERCENT','AMOUNT') NOT NULL,
  `discount_value` float NOT NULL,
  `end_date` datetime NOT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  `is_active` tinyint(1) DEFAULT NULL,
  `created_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vouchers`
--

LOCK TABLES `vouchers` WRITE;
/*!40000 ALTER TABLE `vouchers` DISABLE KEYS */;
INSERT INTO `vouchers` VALUES ('HANGY_00','PERCENT',6,'2026-09-25 01:03:32',1,1,'2026-04-11 01:03:32'),('HANGY_01','AMOUNT',31000,'2026-12-05 01:03:32',2,1,'2026-04-11 01:03:32'),('HANGY_02','PERCENT',13,'2026-07-05 01:03:32',3,1,'2026-04-11 01:03:32'),('HANGY_03','AMOUNT',24000,'2026-11-21 01:03:32',4,1,'2026-04-11 01:03:32'),('HANGY_04','PERCENT',22,'2027-02-22 01:03:32',5,1,'2026-04-11 01:03:32'),('HANGY_05','AMOUNT',62000,'2026-11-01 01:03:32',6,1,'2026-04-11 01:03:32'),('HANGY_06','PERCENT',6,'2026-07-31 01:03:32',7,1,'2026-04-11 01:03:32'),('HANGY_07','AMOUNT',37000,'2026-10-30 01:03:32',8,1,'2026-04-11 01:03:32'),('HANGY_08','PERCENT',22,'2026-10-28 01:03:32',9,1,'2026-04-11 01:03:32'),('HANGY_09','AMOUNT',51000,'2026-08-02 01:03:32',10,1,'2026-04-11 01:03:32'),('HANGY_10','PERCENT',5,'2026-12-20 01:03:32',11,1,'2026-04-11 01:03:32'),('HANGY_11','AMOUNT',31000,'2027-03-12 01:03:32',12,1,'2026-04-11 01:03:32'),('HANGY_12','PERCENT',17,'2026-06-15 01:03:32',13,1,'2026-04-11 01:03:32'),('HANGY_13','AMOUNT',20000,'2026-10-19 01:03:32',14,1,'2026-04-11 01:03:32'),('HANGY_14','PERCENT',28,'2026-12-26 01:03:32',15,1,'2026-04-11 01:03:32'),('HANGY_15','AMOUNT',33000,'2026-06-02 01:03:32',16,1,'2026-04-11 01:03:32'),('HANGY_16','PERCENT',7,'2026-07-22 01:03:32',17,1,'2026-04-11 01:03:32'),('HANGY_17','AMOUNT',36000,'2026-05-21 01:03:32',18,1,'2026-04-11 01:03:32'),('HANGY_18','PERCENT',14,'2026-12-17 01:03:32',19,1,'2026-04-11 01:03:32'),('HANGY_19','AMOUNT',93000,'2027-01-10 01:03:32',20,1,'2026-04-11 01:03:32'),('AAA','AMOUNT',25000,'2026-04-14 18:03:00',21,1,'2026-04-14 18:02:40');
/*!40000 ALTER TABLE `vouchers` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-17 21:11:19
