<?php
$db 		= new PDO("mysql:dbname=DB_NAME;host=localhost","DB_USERNAME","DB_PASS");

$SqlSorgusu = "SELECT * FROM wwphpjQueryResizable WHERE `id` = 1";

$st 		= $db->prepare($SqlSorgusu);

$st->execute();

$Veriler 	= $st->fetchAll(PDO::FETCH_ASSOC);

ECHO $Veriler[0]["width"]."-".$Veriler[0]["height"];

?>