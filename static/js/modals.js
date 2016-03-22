var modalCtn = $('#modal_container'),
	overlay = $('#overlay');

$('document').ready(function() {
	$('.modal_button').click(function() {
		var btnModalVal = $(this).attr('modal-value');
		if (btnModalVal === 'modal_a') {
			buildModalRegistration();
		} else if (btnModalVal === 'modal_b') {
			buildModalLogin();
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
		'<input type="hidden" id="csrfmiddlewaretoken" name="csrfmiddlewaretoken" value="{{ csrf_token }}">'+
		'<div class="modal_header">' +
		'<div class="logo"></div>' +
		'<div class="close_button">&times;</div>' +
		'</div>' +
		'<div class="modal_body">' +
		'<h2 class="title">Registration</h2>' +
		'<div class="input_labl">Username</div>' +
		'<input type="text" required="required" id="username" class="modal_inpt" placeholder="" name="username" title="Enter your full name">' +
		'<div class="input_labl">Email</div>' +
		'<input type="email" required="required" id=""email"" class="modal_inpt" placeholder="" name="email" title="Enter a valid email address">' +
		'<div class="input_labl">Password</div>' +
		'<input type="password" required="required"  id="password" class="modal_inpt" placeholder="" name="password" title="Enter a valid password">' +
		'<div class="input_labl">Confirm Password</div>' +
		'<input type="password" required="required" class="modal_inpt no_margin" placeholder="" name="confirm_password" title="Please confirm password">' +
		'<div class="input_labl">Picture</div>' +
		'<div class="file-upload">'+
		'<label for="upload" class="file-upload__label">Browse</label>'+
		'<input id="upload" class="file-upload__input" type="file" name="profile_picture" accept="/image/*">'+
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
	
	$(document).ready(function() {
		document.getElementById("csrfmiddlewaretoken").value = csrftoken;
		$('#upload').change(function() {
			var filepath = this.value;
			var m = filepath.match(/([^\/\\]+)$/);
			var filename = m[1];
			$('#filename').val(filename);

	});
	});
	
}

function buildModalLogin() {
	var csrftoken = getCookie('csrftoken');
	var html = '<div id="modal_b" class="modal_dialog">' +
		'<form class="modal_form" name="form_a" method="POST" action="/game/login/" enctype="multipart/form-data">' +
		'<input type="hidden" id="csrfmiddlewaretoken" name="csrfmiddlewaretoken" value="{{ csrf_token }}">'+
		'<div class="modal_header">' +
		'<div class="logo"></div>' +
		'<div class="close_button">&times;</div>' +
		'</div>' +
		'<div class="modal_body">' +
		'<h2 class="title">Login</h2>' +
		'<div class="input_labl">Username</div>' +
		'<input type="username" id="username" required="required" class="modal_inpt" placeholder="" name="username" title="Enter a valid email address">' +
		'<div class="input_labl">Password</div>' +
		'<input type="password" id="password" required="required" class="modal_inpt no_margin" placeholder="" name="password" title="Enter a valid password">' +
		'</div>' + 
		'<div class="divide"></div>' +
		'<div class="modal_footer">' +
		'<input type="submit" name="submit" class="modal_button btn_dark btn-full" id="" value="Login">' +
		'</div>' +
		'</form>' +
		'</div>';

	showModal(html);
	
	$(document).ready(function() {
		document.getElementById("csrfmiddlewaretoken").value = csrftoken;
	});
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