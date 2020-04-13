-- phpMyAdmin SQL Dump
-- version 4.0.10.20
-- https://www.phpmyadmin.net
--
-- Anamakine: 94.138.203.100
-- Üretim Zamanı: 11 Nis 2020, 17:40:31
-- Sunucu sürümü: 5.5.52-cll-lve
-- PHP Sürümü: 5.2.17

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Veritabanı: `wwphpdemo`
--

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `wwphpjQueryResizable`
--

CREATE TABLE IF NOT EXISTS `wwphpjQueryResizable` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `width` int(4) NOT NULL,
  `height` int(4) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=2 ;

--
-- Tablo döküm verisi `wwphpjQueryResizable`
--

INSERT INTO `wwphpjQueryResizable` (`id`, `width`, `height`) VALUES
(1, 634, 347);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
