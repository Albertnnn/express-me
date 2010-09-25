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
