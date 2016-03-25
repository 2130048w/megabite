var modalCtn = $('#modal_container'),
	overlay = $('#overlay');

$('document').ready(function() {
	$('.modal_button').click(function() {
		var btnModalVal = $(this).attr('modal-value');
		if (btnModalVal === 'modal_a') {
			buildModalRegistration();
		} else if (btnModalVal === 'modal_b') {
			buildModalLogin();
		} else if(btnModalVal === 'modal_c') {
			buildModalEdit();
		} else if(btnModalVal === 'modal_d'){
			buildModalAbout();
		}

		$('.close_button').addClass('modal_open');
		$(overlay).addClass('modal_open');

		dismissModal();
	});
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function buildModalRegistration() {
	var csrftoken = getCookie('csrftoken');
	var html = '<div id="modal_a" class="modal_dialog">' +
		'<form class="modal_form" name="form_a" id="myForm" method="post" action="/game/register/" enctype="multipart/form-data">' +
		'<input type="hidden" id="csrfmiddlewaretoken" name="csrfmiddlewaretoken" value="'+csrftoken+'">'+
		'<div class="modal_header">' +
		'<div class="logo"></div>' +
		'<div class="close_button">&times;</div>' +
		'</div>' +
		'<div class="modal_body">' +
		'<h2 class="title">Registration</h2>' +
		'<div class="input_labl">Username</div>' +
		'<div class="error" id="username_error"></div>'+
		'<input type="text" required="required" id="username" class="modal_inpt" placeholder="" name="username" title="Enter your full name">' +
		'<div class="input_labl">Email</div>' +
		'<div class="error" id="email_error"></div>'+
		'<input type="email" required="required" id="email" class="modal_inpt" placeholder="" name="email" title="Enter a valid email address">' +
		'<div class="input_labl">Password</div>' +
		'<div class="error" id="password_error"></div>'+
		'<input type="password" required="required"  id="password" class="modal_inpt" placeholder="" name="password" title="Enter a valid password">' +
		'<div class="input_labl">Confirm Password</div>' +
		'<input type="password" required="required" id="cpassword" class="modal_inpt no_margin" placeholder="" name="confirm_password" title="Please confirm password">' +
		'<div class="input_labl">Picture</div>' +
		'<div class="file-upload">'+
		'<label for="upload" class="file-upload__label">Browse</label>'+
		'<input id="upload" class="file-upload__input" type="file" name="profile_picture" accept="images/*">'+
		'</div>'+
		'<input type="text" id="filename" class="modal_inpt" placeholder="Upload a file.." disabled>' +
		'</div>' +
		'<div class="divide"></div>' +
		'<div class="modal_footer">' +
		'<input type="submit" name="submit" class="modal_button btn_dark btn-full" value="register">' +
		'</div>' +
		'</form>' +
		'</div>';
			

	showModal(html);
	
	$('#upload').change(function() {
		var filepath = this.value;
		var m = filepath.match(/([^\/\\]+)$/);
		var filename = m[1];
		$('#filename').val(filename);
	});
	
	$('.modal_button').click(function(event){
	  var un = $('#username').val();
	  var pw = $('#password').val();
	  var cpw = $('#cpassword').val();
	  event.preventDefault();
	  if (pw == cpw) { //The one thing we don't validate in django, might be better to pass this to the view and handle it there, appending it to the errors list
		  var formData = new FormData();
		  formData.append("username", un);
		  formData.append("password", pw);
		  formData.append("email", $('#email').val());
		  formData.append("profile_picture", $('#upload')[0].files[0]); //Either this or 50 lines of xhtml processing to upload files through ajax 
			$.ajax({
				url : "/game/register/", // the endpoint
				type : "POST", // http method
				data : formData,
				processData: false,  // tell jQuery not to process the data
				contentType: false,   // tell jQuery not to set contentType
				
				success : function(data) {
					if (data.reg == true) {
						showRegSuccess(un, pw);
					}
					else {
						$('#username_error').html('')
						$('#password_error').html('')
						$('#email_error').html('')
						if (data.errors) {
							for (i in data.errors) {
								if (i == 'username') {
									$('#username_error').append(data.errors[i])
								}
								else if (i == 'password') {
									$('#password_error').append(data.errors[i])
								}
								else if (i == 'email') {
									$('#email_error').append(data.errors[i])
								}
							}
						}
					}
				},
				
				error : function(xhr,errmsg,err) {
					console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console - THIS HELPED ME SOOO MUCH
				}
			});
		}
		else {
			$('#password_error').html('Passwords have to match');
		}
	});
}

function showRegSuccess(un, pw) {
	var csrftoken = getCookie('csrftoken');
	var html = '<div id="modal_a" class="modal_dialog">' +
		'<form class="modal_form" name="form_a" id="myForm" method="post" action="/game/register/" enctype="multipart/form-data">' +
		'<input type="hidden" id="csrfmiddlewaretoken" name="csrfmiddlewaretoken" value="'+csrftoken+'">'+
		'<div class="modal_header">' +
		'<div class="logo"></div>' +
		'<div class="close_button">&times;</div>' +
		'</div>' +
		'<div class="modal_body">' +
		'<h2 class="title">Registration</h2>' +
		'<div class="input_labl">Succesfully registered</div>' +
		'Thanks for registering '+un+'. We will now log you in.'+
		'<div class="modal_footer">' +
		'<input type="submit" name="submit" class="modal_open modal_button btn_dark btn-full" value="OK">' +
		'</div>' +
		'</form>' +
		'</div>';
			

	modalCtn.html(html);
	$('.modal_open').click(function(event) {
		event.preventDefault();
		ajaxLogin(un, pw)
	});
	
}

function buildModalLogin() {
	var csrftoken = getCookie('csrftoken');
	var html = '<div id="modal_b" class="modal_dialog">' +
		'<form class="modal_form" name="form_a" method="POST" action="/game/login/" enctype="multipart/form-data">' +
		'<input type="hidden" id="csrfmiddlewaretoken" name="csrfmiddlewaretoken" value="'+csrftoken+'">'+
		'<div class="modal_header">' +
		'<div class="logo"></div>' +
		'<div class="close_button">&times;</div>' +
		'</div>' +
		'<div class="modal_body">' +
		'<h2 class="title">Login</h2>' +
		'<div class="input_labl">Username</div>' +
		'<div class="error" id="username_error"></div>'+
		'<input type="username" id="username" required="required" class="modal_inpt" placeholder="" name="username" title="Enter a valid email address">' +
		'<div class="input_labl">Password</div>' +
		'<div class="error" id="password_error"></div>'+
		'<input type="password" id="password" required="required" class="modal_inpt no_margin" placeholder="" name="password" title="Enter a valid password">' +
		'</div>' + 
		'<div class="divide"></div>' +
		'<div class="modal_footer">' +
		'<input type="submit" name="submit" class="modal_button btn_dark btn-full" id="" value="Login">' +
		'</div>' +
		'</form>' +
		'</div>';

	showModal(html);
	
	$('.modal_button').click(function(event){
	  event.preventDefault();
	  ajaxLogin($('#username').val(), $('#password').val());
	});
}

function ajaxLogin(un, pw) {
	$.ajax({
			url : "/game/login/", // the endpoint
			type : "POST", // http method
			data : { username : un, password : pw },
			
			success : function(data) {
				if (data.username_error) {
					$('#username_error').html(data.username_error);
				}
				else if (data.password_error) {
					$('#username_error').html(''); //No username error so we can clear it
					$('#password_error').html(data.password_error); //We don't need to worry about clearing the password error since they will just login
				}
				else if (data.error) {
					alert(data.error) //Account disabled just has an alert
				}
				else {
					window.location.replace('/game/index/'); //redirect them to the index page
				}
			},
			
			error : function(xhr,errmsg,err) {
				console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console - THIS HELPED ME SOOO MUCH
			}
		});
}

function buildModalAchievement(name, desc, pic) {
	var html = '<div id="modal_b" class="modal_dialog">' +
		'<div class="modal_header">' +
		'<div class="logo"></div>' +
		'<div class="close_button">&times;</div>' +
		'</div>' +
		'<div class="modal_body">' +
		'<h2 class="title">Achievement unlocked</h2>' +
		'<div class="input_labl">'+name+'</div>' +
		'<img src='+pic+' alt="A shiny badge">' +
		'<div class="input_labl">'+desc+'</div>' +
		'<div class="modal_footer">' +
		'<input type="submit" name="submit" class="modal_button btn_dark btn-full" id="closebtn" value="OK">' +
		'</div>' +
		'</form>' +
		'</div>';

	showModal(html);
}

function buildModalEdit() {
	var csrftoken = getCookie('csrftoken');
	var html = '<div id="modal_c" class="modal_dialog">' +
		'<form class="modal_form" name="form_a" id="myForm" method="post" action="/game/edit_profile/" enctype="multipart/form-data">' +
		'<input type="hidden" id="csrfmiddlewaretoken" name="csrfmiddlewaretoken" value="'+csrftoken+'>'+
		'<div class="modal_header">' +
		'<div class="logo"></div>' +
		'<div class="close_button">&times;</div>' +
		'</div>' +
		'<div class="modal_body">' +
		'<h2 class="title">Edit</h2>' +
		'<div class="input_labl">Username</div>' +
		'<input type="text" required="required" id="username" class="modal_inpt" placeholder="" name="username" title="Enter your full name">' +
		'<div class="input_labl">Email</div>' +
		'<input type="email" required="required" id=""email"" class="modal_inpt" placeholder="" name="email" title="Enter a valid email address">' +
		'<div class="input_labl">Password</div>' +
		'<input type="password" required="required"  id="password" class="modal_inpt" placeholder="" name="password" title="Enter a valid password">' +
		'<div class="input_labl">Picture</div>' +
		'<div class="file-upload">'+
		'<label for="upload" class="file-upload__label">Browse</label>'+
		'<input id="upload" class="file-upload__input" type="file" name="profile_picture" accept="/image/*">'+
		'</div>'+
		'<input type="text" id="filename" class="modal_inpt" placeholder="Upload a file.." disabled>' +
		'</div>' +
		'<div class="divide"></div>' +
		'<div class="modal_footer">' +
		'<input type="submit" name="submit" class="modal_button btn_dark btn-full" value="edit">' +
		'</div>' +
		'</form>' +
		'</div>';
			

	showModal(html);
	$('#upload').change(function() {
		var filepath = this.value;
		var m = filepath.match(/([^\/\\]+)$/);
		var filename = m[1];
		$('#filename').val(filename);
	});
}

function buildModalAbout() {
	var html = '<div id="modal_d" class="modal_dialog">' +
		'<div class="modal_header">' +
		'<div class="logo"></div>' +
		'<div class="close_button">&times;</div>' +
		'</div>' +
		'<div class="modal_body">' +
		'<h2 class="about">About</h2>' +
		'<p>Megabite is a game of search and survival</p>' +
		'<p>Your aim is to survive for as long as possible during a zombie apocalypse</p>' +
		'<p>Search through houses for food, ammo and survivors to help you defeat zombies</p>'+
		'<p>GOOD LUCK</p>'+
		'</div>';
		

	showModal(html);
}

function showModal(html) {
	modalCtn.append(html);
	overlay.fadeIn();
	modalCtn.fadeIn();
}

function dismissModal() {
	$('.modal_open').click(function() {
		modalCtn.hide();
		overlay.hide();
		modalCtn.html('');
	});
}