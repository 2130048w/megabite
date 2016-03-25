$(document).ready(function(){
	$('#foo').slideme({
		autoslide: true,
		loop: true,
		autoslideHoverStop : false,
		interval : 4000,
		speed : 2000,
		transition : 'zoom',
		resizable: {
			width: 1920,
			height: 1080,
		}
	});
});
