-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.5.8-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win32
-- HeidiSQL Version:             11.0.0.5919
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for meddesk
CREATE DATABASE IF NOT EXISTS `meddesk` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `meddesk`;

-- Dumping structure for table meddesk.activation
CREATE TABLE IF NOT EXISTS `activation` (
  `userId` int(11) NOT NULL,
  `OTP` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table meddesk.activation: ~4 rows (approximately)
DELETE FROM `activation`;
/*!40000 ALTER TABLE `activation` DISABLE KEYS */;
INSERT INTO `activation` (`userId`, `OTP`) VALUES
	(0, 624299),
	(2, 152049),
	(3, 607123),
	(4, 954448),
	(5, 906852);
/*!40000 ALTER TABLE `activation` ENABLE KEYS */;

-- Dumping structure for table meddesk.chat
CREATE TABLE IF NOT EXISTS `chat` (
  `to` int(11) DEFAULT NULL,
  `from` int(11) DEFAULT NULL,
  `message` text DEFAULT NULL,
  `read` tinyint(4) DEFAULT NULL,
  `timestamp` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table meddesk.chat: ~35 rows (approximately)
DELETE FROM `chat`;
/*!40000 ALTER TABLE `chat` DISABLE KEYS */;
INSERT INTO `chat` (`to`, `from`, `message`, `read`, `timestamp`) VALUES
	(0, 4, 'hi', 1, '14/12/2020 17:06:33'),
	(4, 0, 'Hello buddy! What can I do for you?', 1, '14/12/2020 17:06:36'),
	(0, 4, 'I have fever', 1, '14/12/2020 17:06:47'),
	(4, 0, 'Finding best maternity care center nearby you', 1, '14/12/2020 17:06:50'),
	(4, 0, 'Found <i>Popular Nursing Home</i> which is situated in <i>New Town, Rail (Main Road), Jamtara, Jharkhand-815351</i>. Click <a href="/map?lat=28.648832399999996&lng=77.162813">here</a> to view on map', 1, '14/12/2020 17:06:50'),
	(0, 3, 'hi', 1, '15/12/2020 12:44:26'),
	(3, 0, 'Hola! Tell me What can I do for you?', 1, '15/12/2020 12:44:29'),
	(0, 3, 'I have fever', 1, '15/12/2020 12:44:41'),
	(3, 0, 'Finding best maternity care center nearby you', 1, '15/12/2020 12:44:44'),
	(0, 3, 'I have fever', 1, '15/12/2020 13:27:23'),
	(3, 0, 'Finding best maternity care center nearby you', 1, '15/12/2020 13:27:26'),
	(3, 0, 'Found <i>Samvedna Hospital</i> which is situated in <i>Agwanpur Road, Near Molarband School, Om Enclave, Faridabad, Haryana-121003</i>. Click <a href="/map?lat=28.4926396&lng=77.3271433">here</a> to view on map', 1, '15/12/2020 13:27:26'),
	(0, 4, 'hi', 1, '15/12/2020 13:48:42'),
	(4, 0, 'Hola! Tell me What can I do for you?', 1, '15/12/2020 13:48:46'),
	(0, 4, 'I have fever', 1, '15/12/2020 13:48:54'),
	(4, 0, 'Finding best maternity care center nearby you', 1, '15/12/2020 13:48:58'),
	(4, 0, 'Found <i>Akshayvat and Amarjyoti trauma center</i> which is situated in <i>Near udyog nagar park, Naini, Prayagraj, Uttar pradesh-211008</i>. Click <a href="/map?lat=25.616763&lng=82.114579">here</a> to view on map', 1, '15/12/2020 13:48:58'),
	(0, 4, 'I am pregnant', 1, '17/12/2020 13:43:58'),
	(4, 0, 'Finding best maternity care center nearby you', 1, '17/12/2020 13:44:02'),
	(4, 0, 'Found <i>Popular Nursing Home</i> which is situated in <i>New Town, Rail (Main Road), Jamtara, Jharkhand-815351</i>. Click <a href="/map?lat=28.648832399999996&lng=77.162813">here</a> to view on map', 1, '17/12/2020 13:44:02'),
	(0, 4, 'I have fever', 1, '17/12/2020 14:02:41'),
	(4, 0, 'Finding best maternity care center nearby you', 1, '17/12/2020 14:02:45'),
	(4, 0, 'Found <i>Popular Nursing Home</i> which is situated in <i>New Town, Rail (Main Road), Jamtara, Jharkhand-815351</i>. Click <a href="/map?lat=28.648832399999996&lng=77.162813">here</a> to view on map', 1, '17/12/2020 14:02:45'),
	(0, 4, 'I have fever', 1, '18/12/2020 10:16:39'),
	(4, 0, 'Finding best maternity care center nearby you', 1, '18/12/2020 10:16:44'),
	(4, 0, 'Found <i>Ashirwad Laser and Phaco Eye Hospital</i> which is situated in <i>I. G Office Road, Nehru Chowk, Bilaspur, Chhattisgarh-495555</i>. Click <a href="/map?lat=26.8180732&lng=80.9496051">here</a> to view on map', 1, '18/12/2020 10:16:44'),
	(0, 3, 'I have fever', 1, '18/12/2020 23:48:52'),
	(3, 0, 'Finding best maternity care center nearby you', 1, '18/12/2020 23:48:59'),
	(3, 0, 'Found <i>Ashirwad Laser and Phaco Eye Hospital</i> which is situated in <i>I. G Office Road, Nehru Chowk, Bilaspur, Chhattisgarh-495555</i>. Click <a href="/map?lat=26.8180732&lng=80.9496051">here</a> to view on map', 1, '18/12/2020 23:48:59'),
	(0, 4, 'I am sick', 1, '20/12/2020 00:06:58'),
	(4, 0, 'Finding best maternity care center nearby you', 1, '20/12/2020 00:07:02'),
	(4, 0, 'Found <i>Ashirwad Laser and Phaco Eye Hospital</i> which is situated in <i>I. G Office Road, Nehru Chowk, Bilaspur, Chhattisgarh-495555</i>. Click <a href="/map?lat=26.8180732&lng=80.9496051">here</a> to view on map', 1, '20/12/2020 00:07:02'),
	(0, 3, 'I am sick', 1, '21/12/2020 10:37:48'),
	(3, 0, 'Finding best maternity care center nearby you', 1, '21/12/2020 10:37:52'),
	(3, 0, 'Found <i>Ashirwad Laser and Phaco Eye Hospital</i> which is situated in <i>I. G Office Road, Nehru Chowk, Bilaspur, Chhattisgarh-495555</i>. Click <a href="/map?lat=26.8180732&lng=80.9496051">here</a> to view on map', 1, '21/12/2020 10:37:52');
/*!40000 ALTER TABLE `chat` ENABLE KEYS */;

-- Dumping structure for table meddesk.users
CREATE TABLE IF NOT EXISTS `users` (
  `Name` varchar(30) NOT NULL,
  `Password` mediumtext NOT NULL,
  `Mail` varchar(40) NOT NULL,
  `ProfilePic` varchar(200) NOT NULL,
  `userId` int(11) NOT NULL AUTO_INCREMENT,
  `activeStatus` int(11) NOT NULL,
  `userType` varchar(10) NOT NULL,
  PRIMARY KEY (`userId`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

-- Dumping data for table meddesk.users: ~2 rows (approximately)
DELETE FROM `users`;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` (`Name`, `Password`, `Mail`, `ProfilePic`, `userId`, `activeStatus`, `userType`) VALUES
	('himanshu', '$5$rounds=535000$FeTP4W3AadIZAjLX$YCzzlV.TL8BKBg0.RpmJJDmKULk1CtpyTC/UBwTPJj2', 'singh.sh.shivam@gmail.com', 'static/PROFILE_PIC/Himanshuboard.jpg', 4, 1, 'admin'),
	('AmitSahu', '$5$rounds=535000$62bQOdlFnzssx/w2$py3z8Nh9P8ES/FtYn1wdYnucUFB5MR5nsbnf.TgOcC/', 'amit260898@gmail.com', 'static/PROFILE_PIC/AmitSahuCapture9.PNG', 5, 1, 'user');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
