<?php
try {
	$db 		= new PDO("mysql:dbname=DBNAME;host=localhost","USERNAME","PASS");
	if($_GET["proc"] == "ME")
	{
		$SqlSorgusu = "SELECT * FROM client WHERE lastpingtime < '".(time()-10)."' and gameid = '".$_POST["GameID"]."' and usertype = 'guest'";
		$st 		= $db->prepare($SqlSorgusu);
		$st->execute();
		$Veriler 	= $st->fetchAll(PDO::FETCH_ASSOC);
		if(count($Veriler) > 0)
		{
			$stCli 		= $db->prepare("UPDATE `client` SET `point` = '0' WHERE `id` = '".$Veriler[0]["id"]."'");
			$stCli->execute();
			ECHO $Veriler[0]["id"];
		}else{
			ECHO "FULL";
		}
	}
	if($_GET["proc"] == "LOGIN")
	{
		$SqlSorgusu = "SELECT * FROM client WHERE username = '".$_POST["username"]."' and password = '".$_POST["password"]."'";
		$st 		= $db->prepare($SqlSorgusu);
		$st->execute();
		$Veriler 	= $st->fetchAll(PDO::FETCH_ASSOC);
		if(count($Veriler) > 0)
		{
			ECHO $Veriler[0]["id"]."-".$Veriler[0]["point"]."-".$Veriler[0]["username"];
		}else{
			ECHO "0";
		}
		
	}
	if($_GET["proc"] == "REGISTER")
	{
		$SqlSorgusu = "INSERT INTO `client`(`gameid`, `clix`, `cliy`, `point`, `lastpingtime`, `username`, `password`, `usertype`) VALUES ('1', '100', '628', '0', '0', '".$_POST["username"]."', '".$_POST["password"]."','user');";
		$st 		= $db->prepare($SqlSorgusu);
		$st->execute();
		$id = $db->lastInsertId();
		if($id > 0)
		{
			return $id;
		}else{
			return 0;
		}
	}
	if($_GET["proc"] == "IMHERE")
	{
		$SqlSorgusu = "UPDATE `client` SET `lastpingtime` = '".time()."' WHERE `id` = '".$_POST["CliID"]."'";
		$st 		= $db->prepare($SqlSorgusu);
		$st->execute();
	}
	if($_GET["proc"] == "GETCOIN")
	{
		$CoinLeftArray = array("15", "250", "500", "333", "95", "410", "550", "185", "600", "670");
		$ArrIndex = time();
		$ArrIndex = substr($ArrIndex, -1);
		ECHO $CoinLeftArray[$ArrIndex];
	}
	if($_GET["proc"] == "SCORE")
	{
		$SqlSorgusu = "SELECT * FROM client WHERE lastpingtime > '".(time()-10)."'";
		$st 		= $db->prepare($SqlSorgusu);
		$st->execute();
		$Veriler 	= $st->fetchAll(PDO::FETCH_ASSOC);
		$VeriR = "<div class='col-sm-12'><img src='assets/images/active-users.png'></div><br /><hr />";
		foreach($Veriler as $Veri) { 
		if($_POST["CliID"] == $Veri["id"])
			{
				$VeriR .= "<div class='row' style='padding-top:5px;'><div class='col-sm-3' style='padding-top:5px;'> <img src='assets/images/char1.png'; /> </div> <div class='col-sm-5'> <font style='color:green;'>YOU</font> </div> <div class='col-sm-4'>".$Veri["point"]."</div></div>";
			}else{
				$VeriR .= "<div class='row' style='padding-top:5px;'><div class='col-sm-3'>  <img src='assets/images/char1.png'; /> </div> <div class='col-sm-5'> ".$Veri["username"]." </div> <div class='col-sm-4'>".$Veri["point"]."</div></div>";
			}
		}
		ECHO $VeriR;
	}
	if($_GET["proc"] == "ACTIVE")
	{
		$SqlSorgusu = "SELECT * FROM client  WHERE NOT (`id` = ".$_POST["CliID"].") and lastpingtime > '".(time()-10)."' and gameid = '".$_POST["GameID"]."'";
		$st 		= $db->prepare($SqlSorgusu);
		$st->execute();
		$Veriler 	= $st->fetchAll(PDO::FETCH_ASSOC);
		$VeriR = "";
		foreach($Veriler as $Veri) { 
			$VeriR .= $Veri["id"]."-";
		}
		ECHO $VeriR;
	}
	if($_GET["proc"] == "INACTIVE")
	{
		$SqlSorgusu = "SELECT * FROM client  WHERE NOT (`id` = ".$_POST["CliID"].") and lastpingtime < '".(time()-10)."' and gameid = '".$_POST["GameID"]."'";
		$st 		= $db->prepare($SqlSorgusu);
		$st->execute();
		$Veriler 	= $st->fetchAll(PDO::FETCH_ASSOC);
		$VeriR = "";
		foreach($Veriler as $Veri) { 
			$VeriR .= $Veri["id"]."-";
		}
		ECHO $VeriR;
	}
	if($_GET["proc"] == "PLAYERLOCATION")
	{
		$SqlSorgusu = "SELECT * FROM client WHERE NOT (`id` = ".$_POST["CliID"].")";
		$st 		= $db->prepare($SqlSorgusu);
		$st->execute();
		$Veriler 	= $st->fetchAll(PDO::FETCH_ASSOC);
		$DonecekVeri = "";
		foreach($Veriler as $Veri)
		{
			$DonecekVeri .= $Veri["id"]."-".$Veri["clix"]."-".$Veri["cliy"]."#";
		}
		ECHO $DonecekVeri;
	}
	if($_GET["proc"] == "UPDATEMELOCATION")
	{
		$SqlSorgusu = "UPDATE `client` SET `clix` = '".$_POST["x"]."', `cliy` = '".$_POST["y"]."' WHERE `id` = '".$_POST["CliID"]."'";
		$st 		= $db->prepare($SqlSorgusu);
		$st->execute();
	}
	if($_GET["proc"] == "UPDATEMYSCORE")
	{
		$SqlSorgusu = "UPDATE `client` SET `point` = `point` + 1 WHERE `id` = '".$_POST["CliID"]."'";
		$st 		= $db->prepare($SqlSorgusu);
		$st->execute();
	}
	$db = null;
}catch (PDOException $e) {
     "Error!: " . $e->getMessage() . "<br/>";
    die();
}

?>