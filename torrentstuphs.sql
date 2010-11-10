-- phpMyAdmin SQL Dump
-- version 3.3.7deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Nov 10, 2010 at 04:15 PM
-- Server version: 5.1.49
-- PHP Version: 5.3.3-1ubuntu9.1

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `torrentstuphs`
--

-- --------------------------------------------------------

--
-- Table structure for table `log`
--

DROP TABLE IF EXISTS `log`;
CREATE TABLE IF NOT EXISTS `log` (
  `log_id` int(11) NOT NULL AUTO_INCREMENT,
  `show_id` int(11) NOT NULL,
  `show_torrent` varchar(255) NOT NULL,
  `log_completed` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `log_status` int(11) NOT NULL COMMENT '0=nothing 1=in progress 2=complete',
  `show_hash` varchar(250) NOT NULL,
  PRIMARY KEY (`log_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=44 ;

-- --------------------------------------------------------

--
-- Table structure for table `shows_table`
--

DROP TABLE IF EXISTS `shows_table`;
CREATE TABLE IF NOT EXISTS `shows_table` (
  `show_id` int(11) NOT NULL AUTO_INCREMENT,
  `show_name` varchar(255) NOT NULL,
  `show_regex` varchar(255) NOT NULL,
  `show_start_series` int(11) NOT NULL,
  `show_start_episode` int(11) NOT NULL,
  `show_finished_folder` varchar(255) NOT NULL,
  `show_last_download_series` int(11) NOT NULL,
  `show_last_download_episode` int(11) NOT NULL,
  PRIMARY KEY (`show_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=19 ;
