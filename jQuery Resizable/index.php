<!DOCTYPE html>
<html lang="en">
<head>
	<title>wwPHP.com jQuery Nesne Yeniden Boyutlandırma (resizable) Örneği</title>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">
			  <link rel="stylesheet" href="http://code.jquery.com/ui/1.8.20/themes/base/jquery-ui.css" type="text/css" media="all" />

	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js"></script>
	<script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
	<style>
		#resizable { width: 150px; height: 150px; padding: 0.5em; }
		#resizable h3 { text-align: center; margin: 0; }
	    .ui-resizable-helper { border: 2px dotted #00F; }
	</style>
</head>

<body>
	<div class="container">
	  <h2>wwPHP.com jQuery ile Nesne Yeniden Boyutlandırma Örneği.<br /> jQuery-UI Resizable.</h2>
	  <p>Aşağıda bulunan kutuyu yeniden boyutlayabilirsiniz.Yeniden boyutladıktan sonra kutunun genişlik ve yüksekliği veritabanına kayıt edilir.</p>
	</div>
	<div class="container">
		<pre> 
			<div id="Bilgi"></div> 
		</pre> 
		<div class="ui-widget-content ui-resizable" id="resizable">
			<h3 class="ui-widget-header">Boyutumu Değiştir (:</h3>
		</div>
	</div>
</body>
<script type="text/javascript"> 
$(document).ready(function() { 
    $.get("get.php", function (data) {
        var SplitData = data.split("-");
		$("#resizable").width(SplitData[0]);
		$("#resizable").height(SplitData[1]);
    });     
	$("#resizable").resizable({
		animate: false,
		helper: "ui-resizable-helper",
		stop: function (event, ui) {
			height = $("#resizable").height(); 
			width = $("#resizable").width();
			$("#Bilgi").html("<img src='img/load.gif' alt='uygulanıyor...' />");
			$("#Bilgi").load("set.php?width="+width+"&height="+height); 
		}
	});
}); 
</script>
</html>