function hi_main_show_main_view(){
	unload_body();
	$('body').load('hisocial/main/main.html #main_view',function(){
		$("#main_panel_home_btn").click(hi_main_show_home);
//		$("#main_panel_histatus_btn").click(hi_main_show_home);
		$("#main_panel_hifile_btn").click(hi_hifile_show_hifile_view);
		$("#main_panel_logout_btn").click(hi_user_logout);
	});
}

function hi_main_show_home(){
	$('main_content').html("");
}
