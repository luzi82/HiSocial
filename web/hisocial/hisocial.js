$(document).ready(function() {
	if(hi_user_get_user_login_token()==null){
		hi_user_show_auth_view();
	}else{
		hi_main_show_main_view();
	}
});

unload_body_func=null;
function unload_body(){
	if(unload_body_func!=null)
		unload_body_func();
	unload_body_func=null;
}
