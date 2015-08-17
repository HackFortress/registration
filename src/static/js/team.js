console.log("hello")


function check_form() {
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

				switch(input_type) {
					case 'handle':
						if($(this).context.value.match(name_regex)) {
							$(this).context.style.backgroundColor = "white";
							console.log(input_type);
						}
						else{
							$(this).context.style.backgroundColor = "yellow";
						}
						
						break;
					case 'phone':
						if($(this).context.value.match(phone_regex)) {
							$(this).context.style.backgroundColor = "white";
							console.log(input_type);
						}
						else{
							$(this).context.style.backgroundColor = "yellow";
						}
						break;
					case 'email':
						if($(this).context.value.match(email_regex)) {
							$(this).context.style.backgroundColor = "white";
							console.log(input_type);
						}
						else{
							$(this).context.style.backgroundColor = "yellow";
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
		// console.log(player_type,input_type,player_number,team_name)	
		
		
	});	
}
