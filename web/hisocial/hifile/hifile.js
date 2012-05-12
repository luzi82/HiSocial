function hi_hifile_show_hifile_view(){
	$('#main_content').load("hisocial/hifile/hifile.html #hifile_view",function(){
	    $('#hifile_fileupload').fileupload({
	        dataType: 'json',
	        formData: {
	        	PKG:"HiFile",
	        	CMD:"user_upload_torrent",
	        	txtf_user_token_user:hi_user_get_user_login_token()
	        },
	        url: HISOCIAL_JSON_URL,
	        done: function (e, data) {
	        	hi_hifile_refresh_hifile_list();
	        }
	    });
		hi_hifile_refresh_hifile_list();
	});
}

function hi_hifile_refresh_hifile_list(){
	user_login_token=hi_user_get_user_login_token();
	user_id=hi_user_get_user_id();
	if(user_login_token!=null){
		query={
			PKG:"HiFile",
			CMD:"user_list_user_torrent",
			txtf_user_token_user:user_login_token,
			txt_user_id:user_id
		};
		$.post(HISOCIAL_JSON_URL,query,hi_hifile_refresh_hifile_list_0,"json");
	}
}

function hi_hifile_refresh_hifile_list_0(data){
	if(data.result=="ok"){
		torrent_list=data.torrent_list
		len=torrent_list.length;
		l=$('#hifile_list');
		l.html("");
		for(i=0;i<len;++i){
			item=torrent_list[i];
			r=$('<tr>');
				// Name
				d=$('<td>');
					da=$('<a>');
						da.html(item.name);
						da.attr("href","?type=hifile_torrent&torrent_token="+hisocial_escape(item.torrent_token));
					d.append(da)
				r.append(d);
				// Size
				d=$('<td>');
					d.html(hi_hifile_size_string(item.size));
				r.append(d);
				// Seeders
				d=$('<td>');
				r.append(d);
				// Leechers
				d=$('<td>');
				r.append(d);
				// Completed
				d=$('<td>');
				r.append(d);
			l.append(r);
		}
	}else{
		alert("unable to load list");
	}
}

function hi_hifile_size_string(size){
	v=size;
	if(v<1000){
		return v+" B";
	}
	v/=1000;
	if(v<1000){
		return v.toPrecision(3)+" kB";
	}
	v/=1000;
	if(v<1000){
		return v.toPrecision(3)+" MB";
	}
	v/=1000;
	if(v<1000){
		return v.toPrecision(3)+" GB";
	}
	v/=1000;
	if(v<1000){
		return v.toPrecision(3)+" TB";
	}
}

function hi_hifile_show_torrent(){
	unload_body();
	$('body').load('hisocial/hifile/hifile.html #hifile_torrent_view',function(){
		query={
			PKG:"HiFile",
			CMD:"guest_get_torrent_data",
			txtf_HiFile_torrenttoken_torrent:getParameterByName("torrent_token")
		};
		$.post(HISOCIAL_JSON_URL,query,hi_hifile_show_torrent_0,"json");
	});
}

function hi_hifile_show_torrent_0(data){
	if(data.result=="ok"){
		$('#hifile_torrent_view_torrent_link').html(data.value.name);
		$('#hifile_torrent_view_torrent_link').attr("href",HISOCIAL_FILE_URL+"?PKG=HiFile&CMD=guest_get_torrent&txtf_HiFile_torrenttoken_torrent="+hisocial_escape(getParameterByName("torrent_token")));
	}else{
		alert("unable to load data");
	}
}
