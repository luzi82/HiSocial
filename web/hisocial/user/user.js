function hi_user_show_auth_view(){
	unload_body();
	$('body').load('hisocial/user/user.html #auth_view',function(){
		$("#auth_action_type_login").click(hi_user_reset_auth_action);
		$("#auth_action_type_create").click(hi_user_reset_auth_action);
		
		// TODO decide login/create-acc by cookie
		$("input[name=action_type]").val(["login"]);
		hi_user_reset_auth_action();
	});
	unload_body_func=hi_user_close_auth_view;
}

function hi_user_close_auth_view(){
	if(eval("typeof hi_user_"+hi_user_old_action_name+"_hide === 'function'")){
		eval("hi_user_"+hi_user_old_action_name+"_hide")();
	}
	hi_user_old_action_name=null;
}

hi_user_old_action_name=null;
function hi_user_reset_auth_action(){
	action_name=$("input[name=action_type]:checked").val();
	if(action_name==hi_user_old_action_name)return;
	
	if(eval("typeof hi_user_"+hi_user_old_action_name+"_hide === 'function'")){
		eval("hi_user_"+hi_user_old_action_name+"_hide")();
	}
	
	hi_user_old_action_name=action_name;

	if(eval("typeof hi_user_"+action_name+"_show === 'function'")){
		eval("hi_user_"+action_name+"_show")();
	}
}

////////////////////////

function hi_user_createacc_show(){
	$('#action_panel').load('hisocial/user/user.html #createacc_view',function(){
		Recaptcha.create(RECAPTCHA_PUBLIC_KEY,"createacc_captcha_captcha_ctrl",
			{
				theme:"white",
				callback: Recaptcha.focus_response_field
			}
		);
		$("#createacc_form").submit(hi_user_createacc_form_on_submit);
	});
}

function hi_user_createacc_hide(){
	Recaptcha.destroy();
}

function hi_user_createacc_form_on_submit(){
	if($('input[name=txt_password]').val()!=$('input[name=repeat_password]').val()){
		alert("Password not match");
		return false;
	}
	turing_value_t={
		"challenge":Recaptcha.get_challenge(),
		"response":Recaptcha.get_response()
	};
	Recaptcha.destroy();
	turing_value_t=JSON.stringify(turing_value_t);
	$("#turing_value_input").val(turing_value_t);
	hi_user_pending_user_id=$('input[name=txt_user_id]').val();
	s=$(this).serialize();
	$.post(HISOCIAL_JSON_URL,s,hi_user_login_form_on_reply,"json");
	return false;
}

//////////////////////////

function hi_user_login_show(){
	$('#action_panel').load('hisocial/user/user.html #login_view',function(){
		$("#login_form").submit(hi_user_login_form_on_submit);
	});
}

function hi_user_login_form_on_submit(){
	hi_user_pending_user_id=$('input[name=txt_user_id]').val();
	s=$(this).serialize();
	$.post(HISOCIAL_JSON_URL,s,hi_user_login_form_on_reply,"json");
	return false;
}

hi_user_pending_user_id=null;
function hi_user_login_form_on_reply(data){
	if(data.result=="ok"){
		$.cookie("user_id",hi_user_pending_user_id); 
		$.cookie("user_login_token",data.value);
		hi_user_pending_user_id=null;
		hi_main_show_main_view();
	}else{
		hi_user_pending_user_id=null;
		// TODO should show suitable reply?
		hi_user_show_auth_view();
	}
}

///////////////////////

function hi_user_logout(){
	$.cookie("user_id",null);
	$.cookie("user_login_token",null);
	hi_user_pending_user_id=null;
	hi_user_show_auth_view();
}

function hi_user_get_user_login_token(){
	return $.cookie("user_login_token");
}

function hi_user_get_user_id(){
	return $.cookie("user_id");
}
