$(document).ready(function() {
	setUpPage()
});

function setUpPage() {

    // AJAX POST
    $('.ajax-button').click(function(event){
	  event.preventDefault();
	  var value = this.value;
	  showLoading();
        $.ajax({
        url : "/game/play/", // the endpoint
        type : "POST", // http method
        data : { the_post : value }, // data sent with the post request

        // handle a successful response
        success : function(data) {
				var csrftoken = getCookie('csrftoken');
				var html = ''
				if (data.tleft) {
					html += '<div id="overlay"></div><h3>Time until nightfall: '+data.tleft+'</h3>'
				}
				if (data.zombies) {
					html += '<h3>You are being attacked by '+data.zombies+' zombies!</h3></br>'+
							'<img src="/media/images/zom.png" width="190" height="270"></br>'
				}
				else if (data.roomData) {
					html += '<h3>Inside house: '+data.currentHouse+'</h3></br>'
				}
				else if (data.streetData) {
					html += '<h3>'+data.currentStreet+'</h3></br>'
				}
				if (data.state) {
					html += '<h3>'+data.state+'</h3>'
				}
					html += '<h3>'+data.status+'</h3>'
				if (data.newday) {
					html += '<h3>Night has fallen. Your party grows hungry.</h3>'
				}
				if (data.gameover) {
						html +='<h3>You died. Game over.</h3>'
					}
				html += '<form action="" method="post">'+
				'<input type="hidden" id="csrfmiddlewaretoken" name="csrfmiddlewaretoken" value='+csrftoken+'>'+
				'<h3 class="options"> OPTIONS </h3>'+
				'<div>'
				if (data.newday) {
					html +='<input type="submit" class="gamebutton ajax-button" name="continue" value="Continue"/>'
				}
				if (data.gameover) {
					html +='<input type="submit" class="gamebutton ajax-button" name="continue" value="Continue"/>'
				}
				for (i in data.options) {
					if (i != 0 || data.zombies) { //First option is obsolete with our navigation and I'm too lazy to filter it out in views.py - This file was already open
						html += '<input type="submit" class="gamebutton ajax-button inline" name='+data.options[i]+' value='+data.options[i]+' />'
						}
				}
					html+= '</div>'
				if (data.streetData) {
					html += '<div>'+
							'<h3> Street map </h3>'
					for (i in data.streetData) {
						html+= '<input type="image" src="/media/images/h'+data.streetData[i]+'.png" width="200" height="200" class="ajax-button inline" name='+i+' value='+i+' />'
					}	
					html += '</div>'
				}
				if (data.roomData) {
					html += '<div>'+
							'<h3> House map </h3>'
					for (i in data.roomData) {
						html+= '<input type="image" src="/media/images/rooms/r'+data.roomData[i]+'.png" width="200" height="200" class="ajax-button inline" name='+i+' value='+i+' />'
					}
					html+= '</div>'
					}
				html += '</form>'
				$('#game_container').html(html);
				overlay.hide();
				if (data.adata.achieve == true) {
					buildModalAchievement(data.adata.badge, data.adata.desc, data.adata.icon);
					$('.close_button').addClass('modal_open');
					$('#closebtn').addClass('modal_open');
					$(overlay).addClass('modal_open');
					dismissModal();
				}
				setUpPage(); 
            },

        // handle a non-successful response
		
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console - THIS HELPED ME SOOO MUCH
		}
        });
	})
	
	function showLoading() {
	//$('#overlay').fadeIn(); too aggressive on the eyes
	$('#game_container').append('<div class="loadcorner">'+
								'<div class="outer">'+
								'</div>'+
								'<div class="inner">'+
								'</div>'+
								'<div class="inner2">'+
								'</div>'+
								'<div class="inner3">'+
								'</div>'+
								'</div>');
}



    // CSRF code
    function getCookie(name) {
        var cookieValue = null;
        var i = 0;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (i; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    }); 


}