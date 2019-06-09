/*
Navicat MySQL Data Transfer

Source Server         : local
Source Server Version : 80011
Source Host           : localhost:3306
Source Database       : finance

Target Server Type    : MYSQL
Target Server Version : 80011
File Encoding         : 65001

Date: 2019-06-09 23:02:47
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for daily_price
-- ----------------------------
DROP TABLE IF EXISTS `daily_price`;
CREATE TABLE `daily_price` (
  `id` int(11) NOT NULL,
  `data_vendor_id` int(11) NOT NULL,
  `symbol_id` int(11) NOT NULL,
  `price_date` datetime NOT NULL ON UPDATE CURRENT_TIMESTAMP,
  `open_price` decimal(19,4) DEFAULT NULL,
  `high_price` decimal(19,4) DEFAULT NULL,
  `low_price` decimal(19,4) DEFAULT NULL,
  `close_price` decimal(19,4) DEFAULT NULL,
  `adj_close_price` decimal(19,4) DEFAULT NULL COMMENT '调整后的收盘价(复权操作)',
  `volumn` bigint(20) DEFAULT NULL,
  `created_date` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `update_date` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `index_vendor_id` (`data_vendor_id`) USING BTREE,
  UNIQUE KEY `index_symbol_id` (`symbol_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for data_vendor
-- ----------------------------
DROP TABLE IF EXISTS `data_vendor`;
CREATE TABLE `data_vendor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `website_url` varchar(255) DEFAULT NULL COMMENT '平台名字',
  `support_email` varchar(255) DEFAULT NULL,
  `create_date` datetime NOT NULL ON UPDATE CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for exchange
-- ----------------------------
DROP TABLE IF EXISTS `exchange`;
CREATE TABLE `exchange` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `abbrev` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `city` varchar(255) DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  `currency` varchar(64) DEFAULT NULL COMMENT '货币',
  `timezone_offset` time DEFAULT NULL COMMENT '时间校准',
  `created_date` datetime NOT NULL ON UPDATE CURRENT_TIMESTAMP,
  `update_date` datetime NOT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for stock_daily
-- ----------------------------
DROP TABLE IF EXISTS `stock_daily`;
CREATE TABLE `stock_daily` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(32) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `price_date` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `open_price` decimal(19,4) DEFAULT NULL,
  `high_price` decimal(19,4) DEFAULT NULL,
  `low_price` decimal(19,4) DEFAULT NULL,
  `close_price` decimal(19,4) DEFAULT NULL,
  `adj_close_price` decimal(19,4) DEFAULT NULL COMMENT '复权价格，具体情况看是前复权还是后复权',
  `vol` decimal(19,4) DEFAULT NULL COMMENT '成交量',
  `amount` decimal(19,4) DEFAULT NULL COMMENT '成交额',
  `create_date` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `update_date` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33782 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for symbol
-- ----------------------------
DROP TABLE IF EXISTS `symbol`;
CREATE TABLE `symbol` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `exchange_id` int(11) DEFAULT NULL,
  `ticker` varchar(32) DEFAULT NULL COMMENT '股票代码',
  `instrument` varchar(64) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `sector` varchar(255) DEFAULT NULL,
  `currency` varchar(32) DEFAULT NULL,
  `create_date` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `update_date` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `index_exchange_id` (`exchange_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
