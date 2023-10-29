function add_venture(){
	var name1=document.getElementById("Vname").value;
	var loc=document.getElementById("Vlocation").value;
	var stt=document.getElementById("Vstate").value;
	var dist=document.getElementById("Vdistrict").value;
	var pin=document.getElementById("Vpincode").value;
	var lat=document.getElementById("Vlatitude").value;
	var lng=document.getElementById("Vlongitude").value;
	var xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function() {
		document.getElementById("Vname").value=null;
		document.getElementById("Vlocation").value=null;
		document.getElementById("Vstate").value=null;
		document.getElementById("Vdistrict").value=null;
		document.getElementById("Vpincode").value=null;
		document.getElementById("Vlatitude").value=null;
		document.getElementById("Vlongitude").value=null;

	 };
	request="/add_venture?name="+name1+"&loc="+loc+"&state="+stt+"&dist="+dist+"&pin="+pin+"&lat="+lat+"&lng="+lng;
	xmlhttp.open("GET", request, true);
	xmlhttp.send();
}


function showVenture(){
	var pat=document.getElementById("pattern").value;
	var xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function() {
		var temp=this.responseText;
		if(temp.length>0){
			//alert(temp.length);
 			document.getElementById("vents").innerHTML = this.responseText;
		}
 	};
	if(pat.length==0){
		xmlhttp.open("GET", "/vents_fetch?pattern=EMPTY", true);
	}
	else{
		xmlhttp.open("GET", "/vents_fetch?pattern="+pat, true);
	}
	xmlhttp.send();

}

/*function showLinks(){
	var xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function() {
		var temp=this.responseText;
		if(temp.length>0){
			//alert(temp.length);
 			document.getElementById("links").innerHTML = this.responseText;
		}
 	};
 	xmlhttp.open("GET", "/links_fetch", true);
	xmlhttp.send();
}*/

function loadOpt(){
	var mode=document.getElementById("mode").value;
	//alert(mode);
	var formelmt=document.getElementById("cc");
	if(mode=="pass"){
		formelmt.innerHTML='<table><tr><td><b>New Password</b></td><td><input type="password" name="pass" id="pass" placeholder="Password"></td></tr><tr><td><b>(re-Type)New Password</b></td><td><input type="password" id="repass" name="repass" placeholder="Retype password"></td></tr><tr><td><input type="submit" value="Change" onClick="changePass()" class="activate"></td><td><input type="reset" value="Cancel" class="deactivate"></td></tr></table><div id="passcheck"></div>';
	}
	else if(mode=="uname"){
		formelmt.innerHTML='<table><tr><td><b>New User Name</b></td><td><input type="text" id="uname" name="uname" placeholder="User Name"></td></tr><tr><td><b>(re-Type)New User Name</b></td><td><input type="text" id="reuname" name="reuname" placeholder="Retype User Name"></td></tr><tr><td><input type="submit" value="Change" onClick="changeUname()" class="activate"></td><td><input type="reset" value="Cancel" class="deactivate"></td></tr></table><div id"unamecheck"></div>';
	}
	else if(mode=="profpic"){
		formelmt.innerHTML='<form method="post" enctype="multipart/form-data" onSubmit="return validateUpload()" action="changeProfPic"><table><tr><td><b>New Profile Picture</b></td><td><input type="file" id="profpic" name="profpic" onChange="validateUpload()" name="profpic"></td></tr><tr><td><input type="submit" value="Change" class="activate"></td><td><input type="reset" value="Cancel" class="deactivate"></td></tr></table></form><div id="filecheck"></div>';
	}

}

function validateUpload(){
	var fInput = document.getElementById("profpic")
	var flag = 0
	if(fInput.value.length!=0){
		/* file validation */
		var validExt= /(\.jpg|\.jpeg|\.png|\.gif)$/i;
		if (!validExt.exec(fInput.value)) {
			document.getElementById("filecheck").innerHTML='<font color="red">Only JPEG, JPG, PNG and GIF formats are supported!</font>';
fInput.style.borderColor="red";
			flag=0;
		}
		else{
			document.getElementById("filecheck").innerHTML='<font color="green">Looks good!</font>';
			flag=1;
fInput.style.borderColor="green";
		} 
	}
	if(flag==0){
		return false;
	}
	else{
		return true;
	}

}

function changePass(){
	var npass=document.getElementById("pass");
	var renpass=document.getElementById("repass");
	if(repass.value==npass.value){
		if (npass.length<6 || npass.length>15) {
			document.getElementById("passcheck").innerHTML='<font color="red">length of Password should be in between 6-15 characters!</font>';
			npass.style.borderColor="red";
			renpass.style.borderColor="red";
		}
		else{
			var xmlhttp = new XMLHttpRequest();
			xmlhttp.onreadystatechange = function() {
				document.getElementById("passcheck").innerHTML='<font color="green">Password successfully changed!</font>';
				npass.value=null;
				renpass.value=null;
 			};
			xmlhttp.open("GET", "/change_credit?value="+npass.value+"&mode=1", true);   // mode 1 means change password.
			xmlhttp.send();
		
		}
		
	}
	else{
		document.getElementById("passcheck").innerHTML='<font color="red">Password and retyped password not matching!</font>';
		npass.style.borderColor="red";
		renpass.style.borderColor="red";

	}

}

function changeUname(){
	var nuname=document.getElementById("uname");
	var renuname=document.getElementById("reuname");
	if(nuname.value==renuname.value){
		if (nuname.length<5 || renuname.length>20) {
			document.getElementById("unamecheck").innerHTML='<font color="red">length of User name should be in between 5-20 characters!</font>';
			nuname.style.borderColor="red";
			renuname.style.borderColor="red";
		}
		else{
			var xmlhttp = new XMLHttpRequest();
			xmlhttp.onreadystatechange = function() {
				document.getElementById("unamecheck").innerHTML='<font color="green">User Name successfully changed!</font>';
				nuname.value=null;
				renuname.value=null;
 			};
			xmlhttp.open("GET", "/change_credit?value="+nuname.value+"&mode=2", true);   // mode 2 means change username.
			xmlhttp.send();
		
		}
		
	}
	else{
		document.getElementById("unamecheck").innerHTML='<font color="red">User Name and retyped User Name not matching!</font>';
		nuname.style.borderColor="red";
		renuname.style.borderColor="red";

	}

}


function activate(id){
	var xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function() {
 	};
 	xmlhttp.open("GET", "/activate_user?userId="+id, true);
 	xmlhttp.send();

	getUsers();

}

function addIntent(){
	var tagi=document.getElementById("tag").value;
	var pat=document.getElementById("pattern").value;
	var res=document.getElementById("responses").value;
	var act=document.getElementById("action").value;
	var cxt=document.getElementById("context").value;

	var xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function() {
		document.getElementById("tag").value=null;
		document.getElementById("pattern").value=null;
		document.getElementById("responses").value=null;
		document.getElementById("action").value=null;
		document.getElementById("context").value=null;

	 };
	var request="/add_intent?tag="+tagi+"&pat="+pat+"&res="+res+"&act="+act+"&cxt="+cxt;
 	xmlhttp.open("GET", request, true);
	xmlhttp.send();

}

function getIntents(){
	var xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function() {
		var temp=this.responseText;
		if(temp.length>0){
 			document.getElementById("intents_data").innerHTML = this.responseText;
		}
 	};
	xmlhttp.open("GET", "/intents_fetch", true);
	xmlhttp.send();


}


function deactivate(id){
	var xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function() {
 	};
	xmlhttp.open("GET", "/deactivate_user?userId="+id, true);
	xmlhttp.send();

	getUsers();
}

function getUsers(){
	var xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function() {
		var temp=this.responseText;
		if(temp.length>0){
 			document.getElementById("users_data").innerHTML = this.responseText;
		}
 	};
	xmlhttp.open("GET", "/user_fetch", true);
	xmlhttp.send();

}



function del_venture(){
	var name=document.getElementById("Vname").value;
	var loc=document.getElementById("Vlocation").value;
	var stt=document.getElementById("Vstate").value;
	var dist=document.getElementById("Vdistrict").value;
	var pin=document.getElementById("Vpincode").value;
	var lat=document.getElementById("Vlatitude").value;
	var lng=document.getElementById("Vlongitude").value;
	var xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function() {
		document.getElementById("Vname").value=null;
		document.getElementById("Vlocation").value=null;
		document.getElementById("Vstate").value=null;
		document.getElementById("Vdistrict").value=null;
		document.getElementById("Vpincode").value=null;
		document.getElementById("Vlatitude").value=null;
		document.getElementById("Vlongitude").value=null;

	};
	request="/del_venture?name="+name+"&loc="+loc+"&state="+stt+"&dist="+dist+"&pin="+pin+"&lat="+lat+"&lng="+lng;
	xmlhttp.open("GET", request, true);
	xmlhttp.send();

}

function chat_post(){
	var msg=document.getElementById("msg").value;
	var xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function() {
		document.getElementById("msg").value=null;
 	};
	xmlhttp.open("GET", "/chat_post?msg="+msg, true);
	xmlhttp.send();
}

function chat_fetch(){
	var xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function() {
		var temp=this.responseText;
		if(temp.length>0){
 			document.getElementById("chatlets").innerHTML = this.responseText;
		}
 	};
	xmlhttp.open("GET", "/chat_fetch", true);
	xmlhttp.send();
}

function validate(){
	var fInput=document.getElementById("profilePic");
	var email=document.getElementById("email");
	var userId=document.getElementById("userId");
	var password=document.getElementById("password");
	var flag=0;
	if(fInput.value.length!=0){
		/* file validation */
		var validExt= /(\.jpg|\.jpeg|\.png|\.gif)$/i;
		if (!validExt.exec(fInput.value)) {
			document.getElementById("filecheck").innerHTML='<font color="red">Only JPEG, JPG, PNG and GIF formats are supported!</font>';
fInput.style.borderColor="red";
			flag=0;
		}
		else{
			document.getElementById("filecheck").innerHTML='<font color="green">Looks good!</font>';
			flag=1;
fInput.style.borderColor="green";
		} 
        }
	if(email.value.length!=0){
		/* email validation */
		var res=email.value.split('@');
		var ext = /(\.com|\.in|\.ac.in|\.net)$/i;
		if (res[0].length<2 || res[1].length<4 || !ext.exec(res[1]) || res[1]==undefined || res[0]==undefined){
			document.getElementById("emailcheck").innerHTML='<font color="red">Please enter a valid email!</font>';
			flag=0;
email.style.borderColor="red";
		}
		else{
			document.getElementById("emailcheck").innerHTML='<font color="green">Looks good!</font>';
			flag=1;
email.style.borderColor="green";
		} 
        }

	if(userId.value.length!=0){
		/* userId validation */
		var res=userId.value
		if (res.length<5 || res.length>20) {
			document.getElementById("idcheck").innerHTML='<font color="red">Length of User Id should be in between 5-20 characters!</font>';
userId.style.borderColor="red";
			flag=0;
		}
		else{
			document.getElementById("idcheck").innerHTML='<font color="green">Looks good!</font>';
userId.style.borderColor="green";
			flag=1;
		} 
        }

	if(password.value.length!=0){
		/* password validation */
		var res=password.value
		if (res.length<6 || res.length>15) {
			document.getElementById("passcheck").innerHTML='<font color="red">length of Password should be in between 6-15 characters!</font>';
password.style.borderColor="red";
			flag=0;
		}
		else{
			document.getElementById("passcheck").innerHTML='<font color="green">Looks good!</font>';
password.style.borderColor="green";
			flag=1;
		}
	 
        }

if(flag==1){
return true;
}
else{
return false;
}	
}
function validate_login(){
	var userId=document.getElementById("userId");
	var password=document.getElementById("password");
	var flag=0;

	if(userId.value.length!=0){
		/* userId validation */
		var res=userId.value
		if (res.length<5 || res.length>20) {
			document.getElementById("idcheck").innerHTML='<font color="red">&nbsp;&nbsp;&nbsp;&nbsp;Length of User Id should be in between 5-20 characters!</font>';
userId.style.borderColor="red";
			flag=0;
		}
		else{
			document.getElementById("idcheck").innerHTML='<font color="green">&nbsp;&nbsp;&nbsp;&nbsp;Looks good!</font>';
			flag=1;
userId.style.borderColor="green";
		} 
        }

	if(password.value.length!=0){
		/* password validation */
		var res=password.value
		if (res.length<6 || res.length>15) {
			document.getElementById("passcheck").innerHTML='<font color="red">&nbsp;&nbsp;&nbsp;&nbsp;Length of Password should be in between 6-15 characters!</font>';
password.style.borderColor="red";
			flag=0;
		}
		else{
			document.getElementById("passcheck").innerHTML='<font color="green">&nbsp;&nbsp;&nbsp;&nbsp;Looks good!</font>';
			flag=1;
password.style.borderColor="green";
		}
	 
        }

if(flag==1){
return true;
}
else{
return false;
}	

}

function remove_msg(){
	if(document.getElementById("alert alert-success")!=null){
		document.getElementById("alert alert-success").style.display='none';
	}
	if(document.getElementById("alert alert-danger")!=null){
		document.getElementById("alert alert-danger").style.display='none';
	}
}

function getLocation() {
    navigator.geolocation.getCurrentPosition(storePosition);
}

function storePosition(position) {
	var xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function() {
 	};
	xmlhttp.open("GET", "/storePosition?lat="+position.coords.latitude+"&longi="+position.coords.longitude, true);
	xmlhttp.send();
}

