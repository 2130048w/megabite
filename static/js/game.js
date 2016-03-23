$(document).ready(function() {
	setUpPage()
});

function setUpPage() {

    // AJAX POST
    $('.ajax-button').click(function(event){
      console.log('am i called');
	  event.preventDefault();
	  var value = this.value;
        $.ajax({
        url : "/game/play/", // the endpoint
        type : "POST", // http method
        data : { the_post : value }, // data sent with the post request

        // handle a successful response
        success : function(data) {
				console.log(data)
				var csrftoken = getCookie('csrftoken');
				var html = '<h2>Time until nightfall: '+data.tleft+'</h2>'
					if (data.rooms) {
						html += '<h2>Inside house: '+data.currentHouse+'</h2></br>'
					}
					else if (data.street) {
						html += '<h2>'+data.currentStreet+'</h2></br>'
						'<section id="map" size=90vh>' +
       				 	'<div class="container">' + 
						'<div class="maps">'+
						'<div class="collapse navbar-collapse navbar-right">'
						'<ul class="nav navbar-nav">'
						for (i in data.street) {
							html+= '<input type="image" src="/media/images/h'+Math.floor((Math.random()*3))+'.png" width="20%"class="ajax-button file-upload__label" name='+i+' value='+i+' />'
						}	
						'</ul>' +
						'</div>' +
						'</div>' +
						'</div>' +
						'</section>' +
						'</br>'
					}
					else if (data.zombies) {
						html += '<h2>You are being attacked by '+data.zombies+' zombies!</h2></br>'
					}
						html += '<h2>'+data.state+'</h2>'+
						'<h2>'+data.status+'</h2>'+
						'<form action="" method="post">'+
						'<input type="hidden" id="csrfmiddlewaretoken" name="csrfmiddlewaretoken" value='+csrftoken+'>'+
						'<div class="collapse navbar-collapse navbar-right">'+
						'<h2> Options </h2>'+
						'<ul class="nav navbar-nav">'
						for (i in data.options) {
							html += '<li><input type="submit" class="ajax-button file-upload__label" name='+data.options[i]+' value='+data.options[i]+' /></li>'
						}
						html+= '</ul>'+
							   '</div>'
					if (data.street) {
						html += '<div class="collapse navbar-collapse navbar-right">'+
								'<h2> Houses </h2>'+
								'<ul class="nav navbar-nav">'
						for (i in data.street) {
							html+= '<li><input type="submit" class="ajax-button file-upload__label" name='+i+' value='+i+' /></li>'
						}
						html+= '</ul>'+
							   '</div>'
					}
					if (data.rooms) {
						html += '<div class="collapse navbar-collapse navbar-right">'+
								'<h2> Rooms </h2>'+
								'<ul class="nav navbar-nav">'
						for (i in data.rooms) {
							html+= '<li><input type="image" src="/media/images/rooms/r'+Math.floor((Math.random()*i))+'.png" class="ajax-button file-upload__label" name='+i+' value='+i+' /></li>'
						}
						html+= '</ul>'+
							   '</div>'
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
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
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