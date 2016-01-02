function check_form() {
	var team={'tf2':{},'hack':{}}
	error=0
	$("#team_form :input").each(function( index ) {
		// console.log($(this).context.id);
		var name_regex= new RegExp(/[\S]{1,20}$/);
		var email_regex= new RegExp(/\S*\@\S*\.\S{1,}$/);
		var phone_regex= new RegExp(/\d{0,2}-\d{3}-\d{3}-\d{4}$|\d{3}-\d{3}-\d{4}$/);

		if ($(this).context.id == 'team') {
			team_name=$(this).context.value
		}
		else {
			var match=$(this).context.id.match(/(^\S{3,4})\_(\S*)\_(\d{1,3}$)/)
			if (match) {
				var player_type=match[1]
				var input_type=match[2]
				var player_number=match[3]
				if (team[player_type][player_number]==undefined) {
					team[player_type][player_number]={}
				}
				switch(input_type) {
					case 'handle':
						if($(this).context.value.match(name_regex) || $(this).context.value == '') {
							$(this).context.style.backgroundColor = "white";
							team[player_type][player_number]['handle']=$(this).context.value
						}
						else{
							$(this).context.style.backgroundColor = "yellow";
							error=1
						}
						
						break;
					case 'phone':
						if($(this).context.value.match(phone_regex) || $(this).context.value == '') {
							$(this).context.style.backgroundColor = "white";
							team[player_type][player_number]['phone']=$(this).context.value
						}
						else{
							$(this).context.style.backgroundColor = "yellow";
							error=1
						}
						break;
					case 'email':
						if($(this).context.value.match(email_regex) || $(this).context.value == '') {
							$(this).context.style.backgroundColor = "white";
							team[player_type][player_number]['email']=$(this).context.value
						}
						else{
							$(this).context.style.backgroundColor = "yellow";
							error=1
						}
						break;
					default:
						return true;
				}
			}
		}
		if(team_name=='') {
			$("#team").css("background","yellow");
		}
		else {
			$("#team").css("background","white");
		}
		
		
	});	
	if(team_name!='' && error==0) {
		message={'name':team_name,'members':team}
		var request = $.ajax({
			type: "POST",
			url: "/register_team",
		    data: JSON.stringify(message),
		    contentType: "application/json; charset=utf-8",
		    dataType: "json"
		});

		request.done(function( msg ) {
			console.log(msg)
			$().toastmessage('showToast', {
			    text     : msg['message'],
			    sticky   : true,
			    position : 'middle-center',
			    type     : 'success',
			    close    : function () {window.location.reload(false);}
			});
		});
		 
		request.fail(function( msg ) {
	        $().toastmessage('showToast', {
			    text     : msg['responseJSON']['message'],
			    sticky   : true,
			    position : 'middle-center',
			    type     : 'error',
			    close    : function () {console.log("toast is closed ...");}
			});
		});
	}
	else {
		console.log("Form Error")
	}
	
}