$(document).ready(function(){		
	var Players 	= [];
	var MECoorX	= 0;
	var MECoorY	= 0;
	var MEID 	= 0; 
	var ThisGameID 	= "1";

// USER COOKIE GET FUNCTION
function getCookie(cname) {
	var name = cname + "=";
	var decodedCookie = decodeURIComponent(document.cookie);
	var ca = decodedCookie.split(';');
	for(var i = 0; i <ca.length; i++) {
		var c = ca[i];
		while (c.charAt(0) == ' ') {
			c = c.substring(1);
		}
		if (c.indexOf(name) == 0) {
			return c.substring(name.length, c.length);
		}
	}
	return "";
}
	
// USER COOKIE SET FUNCTION
function setCookie(cname, cvalue, exdays) {
	var d = new Date();
	d.setTime(d.getTime() + (exdays*24*60*60*1000));
	var expires = "expires="+ d.toUTCString();
	document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}
	
	// USER COOKIE CONTROL
	var UserCookie = getCookie("wwGameUser");
	
	if(UserCookie != "") // IF Cookie ISSET
	{
		var UserCookieDataSplit = UserCookie.split("-"); // SPLIT COOKIE DATA
		var UserName = UserCookieDataSplit[0];
		var Password = UserCookieDataSplit[1];
		$.post("process.php?proc=LOGIN", // POST UserName and Password process.php?proc=LOGIN page
		{
			username:UserName,
			password:Password
		},
		function(data,status){	
			if(data != "0") // Return data if not equals 0 Username and Password correct
			{
				var DataSplit = data.split("-"); // Split return User data.
				MEID = DataSplit[0]; // Update MEID
				document.getElementById("MyScore").innerHTML 		= DataSplit[1]; // Show MyScore div in user latest score.
				document.getElementById("login").style.display 		= "none"; // Hide User Login Box.
				document.getElementById("afterlogin").style.display = "block"; // Show Afterlogin Box.
				document.getElementById("usernameDiv").innerHTML 	= DataSplit[2]; // Change Afterlogin Username div content.
				setCookie("wwGameUser", UserName+"-"+Password, 2); // SET User Cookie 2 days.
				
			}else{
				alert("Username or Password Incorrect.");
			}
		});
	}else{
		// IF User not set cookie and not login set guest account this user.
		$.post("process.php?proc=ME",
		{
			GameID:ThisGameID
		},
		function(data,status){
			if(data == "FULL") // IF all guest account is used show message user screen "Guest Account FULL !" message and MEOBJ hidden.
			{
				alert("Guest Account FULL !");
				document.getElementById("MEOBJ").style.display = "none";
			}else{
				if(MEID == 0)
				{
					MEID = data;
				}
			}
		});
	}
	
	// LOGIN BUTTON CLICK
	$( "#loginBtn" ).click(function() {
		var UserName = document.getElementById('username').value; // Username INPUT Value
		var Password = document.getElementById('password').value; // Password INPUT Value
		if(UserName != "" && Password != "") // IF NOT EMPTY Username and Password Input
		{
			$.post("process.php?proc=LOGIN", // POST User data to process.php?proc=LOGIN page.
			{
				username:UserName,
				password:Password
			},
			function(data,status){	
				if(data != "0") // IF Username and Password correct return data split.
				{
					var DataSplit = data.split("-");
					MEID = DataSplit[0]; // UPDATE MEID 
					document.getElementById("MyScore").innerHTML 		= DataSplit[1]; // Update MyScore latest score.
					document.getElementById("login").style.display 		= "none"; // Login box hide.
					document.getElementById("afterlogin").style.display = "block"; // Show Afterlogin box.
					document.getElementById("usernameDiv").innerHTML 	= DataSplit[2]; // Change Afterlogin Username div content.
					setCookie("wwGameUser", UserName+"-"+Password, 2); // Create Cookie 2 Days
				}else{
					alert("Username or Password Incorrect.");
				}
			});
		}else{
			alert("Username or Password Empty!");
		}
	});
	// REGISTER BUTTON CLICK
	$( "#registerBtn" ).click(function() {
		var UserName = document.getElementById('username').value; // Username INPUT Value
		var Password = document.getElementById('password').value; // Password INPUT Value
		if(UserName != "" && Password != "") // IF NOT EMPTY Username and Password Input
		{
			$.post("process.php?proc=REGISTER", // POST Username and Password data process.php?proc=REGISTER page.
			{
				username:UserName,
				password:Password
			},
			function(data,status){	
				if(data != "0") // IF register return data not equals 0
				{
					MEID = data; // Update MEID.
					document.getElementById("MyScore").innerHTML 		= "0";
					document.getElementById("login").style.display 		= "none"; // Login box hide.
					document.getElementById("afterlogin").style.display = "block"; // Show Afterlogin box.
					document.getElementById("usernameDiv").innerHTML 	= UserName; // Change Afterlogin Username div content.
					setCookie("wwGameUser", UserName+"-"+Password, 2); // Create Cookie 2 Days
				}else{
					alert("Error.");
				}
			});
		}else{
			alert("Username or Password Empty!");
		}
	});
	
	$( "#loginoutBtn" ).click(function() { // LOGOUT Button Click.
		setCookie("wwGameUser", UserName+"-"+Password, -1); // User Cookie Day -1.
		location.reload(); // Content Reload.
	});

	// IM HERE
	// IF I Active Send process.php?proc=IMHERE page.
	setInterval(function(){
		if(MEID > 0)
		{
			$.post("process.php?proc=IMHERE", // POST CliID to process.php?proc=IMHERE.
			{
				GameID:ThisGameID,
				CliID:MEID
			});
		}
	}, 500);
	// SCORE LIST
	setInterval(function(){ // Show Dynamic Active User Score List on #score div content.
		if(MEID > 0)
		{
			$.post("process.php?proc=SCORE",
			{
				GameID:ThisGameID,
				CliID:MEID
			},
			function(data,status){	
				$("#score").html(data);
			});
		}
	}, 500);
	//Active Player Check
	// Check Active Players on 500 Miliseconds
	setInterval(function(){
		if(MEID > 0)
		{
			$.post("process.php?proc=ACTIVE",
			{
				status:"New",
				GameID:ThisGameID,
				CliID:MEID
			},
			function(data,status){
				var ClientDetail = data.split("-"); // ACTIVE Players Data.
				for (ia = 0; ia < ClientDetail.length; ia++) {
					var ClientCheck  = Players.indexOf(ClientDetail[ia]);
					if(ClientCheck < 0 && ClientDetail[ia] != "")
					{
						Players.push(ClientDetail[ia]); // Add Players varibles add Player ID
						$('#gamecontent').append('<img class="" id="PlayerObj'+ClientDetail[ia]+'" style="top:620px; postion:absolute; background:none; border:0px;" src="assets/images/char1_walk.gif"/>'); // ADD Active player character on #gamecontent.
					}
				}
			});
		}
	}, 500);
	//InActive Player Check
	setInterval(function(){
		if(MEID > 0)
		{
			$.post("process.php?proc=INACTIVE",
			{
				status:"New",
				GameID:ThisGameID,
				CliID:MEID
			},
			function(data,status){
				var ClientDetail = data.split("-"); // Inactive Player Data
				for (ia = 0; ia < ClientDetail.length; ia++) {
					var ClientCheck  = Players.indexOf(ClientDetail[ia]);
					if(ClientCheck > -1 && ClientDetail[ia] != "")
					{
						Players = Players.filter(function(item) {
							return item !== ClientDetail[ia];
						});
						$('#PlayerObj'+ClientDetail[ia]+'').remove(); // Remove InActive Player.
					}
				}
			});
		}
	}, 500);
	// Check Players Location
	var LastLocation = 0;
	setInterval(function(){
		if(MEID > 0)
		{
			$.post("process.php?proc=PLAYERLOCATION",
			{
				CliID:MEID,
				GameID:ThisGameID
			},
			function(data,status){		
				var ExpCliDetail = data.split("#");
				for (ia = 0; ia < ExpCliDetail.length; ia++) {
					if(ExpCliDetail[ia] != "")
					{
						var ExpCliDetailLoc = ExpCliDetail[ia].split("-");
						var ClientCheck  = Players.indexOf(ExpCliDetailLoc[0]);
						if(ClientCheck + 1 > 0 )
						{
							LastLocation = document.getElementById("PlayerObj"+ExpCliDetailLoc[0]+"").style.left;
							if(LastLocation < ExpCliDetailLoc[1])
							{
								document.getElementById("PlayerObj"+ExpCliDetailLoc[0]+"").style.transform = "scale(1, 1)";
							}else if(LastLocation > ExpCliDetailLoc[1])
							{
								document.getElementById("PlayerObj"+ExpCliDetailLoc[0]+"").style.transform = "scale(-1, 1)";
							}
							document.getElementById("PlayerObj"+ExpCliDetailLoc[0]+"").style.position = "absolute";
							document.getElementById("PlayerObj"+ExpCliDetailLoc[0]+"").style.top      = ExpCliDetailLoc[2]+"px";
							document.getElementById("PlayerObj"+ExpCliDetailLoc[0]+"").style.left     = ExpCliDetailLoc[1]+"px";
						}
					}
				}
			});
		}
	}, 100);				
	
	// KEYBOARD CONTROL
	$(document).keydown(function(e){
		var offset = $("#MEOBJ").offset();
		var xPos = offset.left; // MEOBJ Left Position
		var yPos = offset.top; // MEOBJ Top Position
		MECoorX = xPos;
		MECoorY = yPos;
		$.post("process.php?proc=UPDATEMELOCATION", // NEW MEOBJ Location Update.
		{
			x:xPos,
			y:yPos,
			CliID:MEID,
			GameID:ThisGameID
		});
		switch (e.which){
			case 37: // LEFT Arrow Key 
				if(MECoorX > 25)
				{
					$("#MEOBJ").finish().animate({ // IF Press Left Arrow Key MEOBJ LEFT : LEFT - 10px
						left: "-=10"
					});
				}
				$("#MEOBJ").addClass('mirror');
				break;
			case 39: //RIGHT Array Key
				if(MECoorX < 700)
				{
					$("#MEOBJ").finish().animate({// IF Press Right Arrow Key MEOBJ RIGHT : RIGHT + 10px
						left: "+=10"
					});
				}
				$("#MEOBJ").removeClass('mirror');
				break;
		}
	});
	//CREATE AND CONTROL COIN
	setInterval(function(){
		if(MEID > 0)
		{
			var CoinPosLeft;
			$.post("process.php?proc=GETCOIN", // GET Coin Position
			{
				CliID:MEID,
				GameID:ThisGameID
			},
			function(data,status){
				CoinPosLeft = data; // Coin Position 
				var CoinID = Math.floor(Math.random() * 700); // Create Random Coin ID
				var Coin = $('<img id="Coin'+CoinID+'" class="coin" style="left:'+(CoinPosLeft)+'px;" src="assets/images/coin.gif"/>');
				Coin.appendTo($('#gamecontent')); // Add NEW Coin on gamecontent.
				Coin.animate({
					top: 650
				}, 
				{ 
					step: function(now, fx){
						var CoinLeft = Coin.offset().left; // Coin Left Position
						var CoinTop  = Coin.offset().top; // Coin Top Position
						if(CoinLeft + 20 > MECoorX && MECoorX + 20 > CoinLeft)
						{
							if(CoinTop + 20 > MECoorY && MECoorY + 20 > CoinTop)
							{
								Coin.remove(); // IF Coin Postion cross the Player position Coin Remove
								$.post("process.php?proc=UPDATEMYSCORE", // Update Player Score.
								{
									CliID:MEID,
									GameID:ThisGameID
								});
								var OldScore = document.getElementById('MyScore').innerHTML; // Old Score
								document.getElementById('MyScore').innerHTML = parseInt(OldScore)+1;  // Update MyScore div content Oldscore + 1
							}
						}
					},
					complete: function(){
						Coin.remove(); // Coin finish animate : top position 650 coin remove.
						CoinLeft = 0;
						CoinTop  = 0;
					},
					duration:4000
				});
			});
		}
	}, 1000);
	var e = jQuery.Event("keydown");
    e.keyCode = 39;                     
    $(document).trigger(e);   
});				