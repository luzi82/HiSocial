function hi_main_show_main_view(){
	unload_body();
	$('body').load('hisocial/main/main.html #main_view',function(){
		$("#main_panel_logout_btn").click(hi_user_logout);
		hi_main_show_main_menu();
	});
}

function hi_main_show_main_menu(){
	$('#main_content').load('hisocial/main/main.html #main_menu',function(){
		//$("#main_menu_histatus_link").click(hi_user_logout);
		//$("#main_menu_hifile_link").click(hi_user_logout);
	});
}
