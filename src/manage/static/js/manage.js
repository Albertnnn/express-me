$(function(){
	$('#menu-bar .app-menu-title').each(function(index){
		//$(this);
	});
});

function toggle_menu(v, no_ani){
  if (v.hasClass('app-menu-show')){
    v.removeClass('app-menu-show');
    v.addClass('app-menu-hide');
    if (no_ani)
      v.next().hide();
    else
      v.next().slideUp();
  }
  else{
    v.removeClass('app-menu-hide');
    v.addClass('app-menu-show');
    if (no_ani)
      v.next().show()
    else
      v.next().slideDown();
  }
}

function set_info(msg){
	m = '#info_msg'
	if (msg) {
		$(m).html(msg).show();
	}
	else {
		$(m).hide();
	}
}

function set_warning(msg){
	m = '#warning_msg'
	if (msg) {
		$(m).html(msg).show();
	}
	else {
		$(m).hide();
	}
}

function set_error(msg){
	m = '#error_msg'
	if (msg) {
		$(m).html(msg).show();
	}
	else {
		$(m).hide();
	}
}
