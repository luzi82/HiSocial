function hi_main_show_main_view(){
	unload_body();
	$('body').load('hisocial/main/main.html #main_view',function(){
		$("#main_panel_logout_btn").click(hi_user_logout);
	});
}
