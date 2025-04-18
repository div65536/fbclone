
function uploadImage(event){
	form = document.getElementById("profile-picture-form")
	form.submit()
}

function uploadCoverImage(event){
	form = document.getElementById("cover-picture-form")
	form.submit()
}

function uploadBio(event){
	form = document.getElementById("bio-upload-form")
	form.submit()
}

function submitSearchForm(event){
	if(event.keyCode==13){
		event.target.submit()
	}
}

function secondNavHandleClick(event){
	id = event.target.id;
	line = document.getElementById("second-nav-line")
	line.remove()
	document.getElementById(id).appendChild(line)
	if(id == "posts"){
		loadPosts()
	}
	else if(id == "about"){
		loadAbout()
	}
	else{
		loadFriends()
	}
}


function loadForm(event){

	let xhr = new XMLHttpRequest()
	xhr.open("GET","posts/createpost")
	xhr.onload = function(){
		document.getElementById
	}
}

function submitPostForm(event){
	form = document.getElementById("create-post-form")
	form.submit()
}
