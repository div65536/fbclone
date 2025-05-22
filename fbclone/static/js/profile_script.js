



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

function saveImage(event){
	id = event.target.dataset.id
	imageInput = document.getElementById(`edit-post-image-field${id}`)
	console.log(document.getElementById(`edit-post-image-field${id}`))
	imageInput.addEventListener('change',function(e){
		console.log(e.target.files)
		const file = e.target.files[0];
		if (file){
			const reader = new FileReader()
			reader.onload = function(e){
				document.querySelector(`.post-image-nested-modal${id}`).src = e.target.result
			}
			reader.readAsDataURL(file)
		}
	})
	
}

function editImage(event){
	postId = event.target.dataset.id
	csrfToken = document.getElementById(`csrftoken-edit${postId}`).value
	let xhr = new XMLHttpRequest()
	xhr.open("POST", `/posts/editpost/${postId}`)
	xhr.setRequestHeader('X-CSRFToken',csrfToken)
	const formData = new FormData()
	imageFile = document.getElementById(`edit-post-image-field${postId}`).files[0]
	caption = document.getElementById(`edit-post-body-field${postId}`).value
	formData.append('file',imageFile)
	formData.append('text',caption)
	xhr.onload = function(){
		if(xhr.status == 200){
			location.reload()
		}
	}
	xhr.send(formData)	
}