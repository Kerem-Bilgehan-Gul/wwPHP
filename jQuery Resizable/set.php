<?php
sleep(1);
$db 		= new PDO("mysql:dbname=DB_NAME;host=localhost","DB_USERNAME","DB_PASS", array(PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION));
try{
	$db->beginTransaction();
	
	$SqlSorgusu = "UPDATE `wwphpjQueryResizable` SET `width` = :width, `height` = :height WHERE `id` = 1";

	$st = $db->prepare($SqlSorgusu);

	$st->bindParam(':width', $_GET["width"]);
	
	$st->bindParam(':height', $_GET["height"]);
		
	$st->execute();

	$db->commit();
	
	ECHO "<div style='color:green; font-size:20px;'>Boyutlandırma Başarılı ! </div>";
}
catch (Exception $e){
	
    if ($db->inTransaction()) {
		
        $db->rollback();
		
    }
	
    ECHO "<div style='color:red; font-size:20px;'>HATA MEYDANA GELDİ ! </div>";
	
}

?>