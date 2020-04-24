-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Anamakine: localhost
-- Üretim Zamanı: 24 Nis 2020, 10:16:59
-- Sunucu sürümü: 10.1.36-MariaDB
-- PHP Sürümü: 7.3.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Veritabanı: `wwphpgame`
--

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `client`
--

CREATE TABLE `client` (
  `id` int(11) NOT NULL,
  `gameid` varchar(45) COLLATE utf8_bin DEFAULT NULL,
  `clix` varchar(45) COLLATE utf8_bin DEFAULT NULL,
  `cliy` varchar(45) COLLATE utf8_bin DEFAULT NULL,
  `point` varchar(45) COLLATE utf8_bin DEFAULT NULL,
  `lastpingtime` int(32) DEFAULT NULL,
  `username` varchar(16) COLLATE utf8_bin DEFAULT NULL,
  `password` varchar(64) COLLATE utf8_bin DEFAULT NULL,
  `usertype` varchar(10) COLLATE utf8_bin DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Tablo döküm verisi `client`
--

INSERT INTO `client` (`id`, `gameid`, `clix`, `cliy`, `point`, `lastpingtime`, `username`, `password`, `usertype`) VALUES
(1, '1', '502.578125', '628', '0', 1587716151, 'Guest1', NULL, 'guest'),
(2, '1', '50', '628', '0', 1587648884, 'Guest2', NULL, 'guest'),
(3, '1', '50', '628', '0', 1587639938, 'Guest3', NULL, 'guest'),
(4, '1', '100', '628', '24', 1587391515, 'Guest4', NULL, 'guest'),
(5, '1', '680', '628', '218', 1587374677, 'Guest5', NULL, 'guest');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `game`
--

CREATE TABLE `game` (
  `id` int(11) NOT NULL,
  `gamename` varchar(45) COLLATE utf8_bin DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dökümü yapılmış tablolar için indeksler
--

--
-- Tablo için indeksler `client`
--
ALTER TABLE `client`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `game`
--
ALTER TABLE `game`
  ADD PRIMARY KEY (`id`);

--
-- Dökümü yapılmış tablolar için AUTO_INCREMENT değeri
--

--
-- Tablo için AUTO_INCREMENT değeri `client`
--
ALTER TABLE `client`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Tablo için AUTO_INCREMENT değeri `game`
--
ALTER TABLE `game`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
