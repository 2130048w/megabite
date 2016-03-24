$(document).ready(function() {
	setUpPage()
});

function setUpPage() {

    // AJAX POST
    $('.ajax-button').click(function(event){
      console.log('am i called');
	  event.preventDefault();
	  var value = this.value;
	  $('#game_container').html('<div id="ajaxloader" class="truecenter"></div>');
        $.ajax({
        url : "/game/play/", // the endpoint
        type : "POST", // http method
        data : { the_post : value }, // data sent with the post request

        // handle a successful response
        success : function(data) {
				console.log(data)
				var csrftoken = getCookie('csrftoken');
				var html = '<h2>Time until nightfall: '+data.tleft+'</h2>'
					if (data.roomData) {
						html += '<h2>Inside house: '+data.currentHouse+'</h2></br>'
					}
					else if (data.streetData) {
						html += '<h2>'+data.currentStreet+'</h2></br>'
					}
					else if (data.zombies) {
						html += '<h2>You are being attacked by '+data.zombies+' zombies!</h2></br>'
					}
						html += '<h2>'+data.state+'</h2>'+
						'<h2>'+data.status+'</h2>'+
						'<form action="" method="post">'+
						'<input type="hidden" id="csrfmiddlewaretoken" name="csrfmiddlewaretoken" value='+csrftoken+'>'+
						'<h2> Options </h2>'+
						'<div>'
						for (i in data.options) {
							html += '<input type="submit" class="ajax-button file-upload__label inline" name='+data.options[i]+' value='+data.options[i]+' />'
						}
						html+= '</div>'
					if (data.streetData) {
						html += '<div>'+
								'<h2> Street map </h2>'
						for (i in data.streetData) {
							html+= '<input type="image" src="/media/images/h'+data.streetData[i]+'.png" width="200" height="200" class="ajax-button inline" name='+i+' value='+i+' />'
						}	
						html += '</div>'
					}
					if (data.roomData) {
						html += '<div>'+
								'<h2> House map </h2>'
						for (i in data.roomData) {
							html+= '<input type="image" src="/media/images/rooms/r'+data.roomData[i]+'.png" width="200" height="200" class="ajax-button inline" name='+i+' value='+i+' />'
						}
						html+= '</div>'
					}
					html += '</form>'
				$('#game_container').html(html);
				if (data.adata.achieve == true) {
					console.log('Got here');
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