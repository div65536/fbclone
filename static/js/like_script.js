

function handleClick(event){
    post_id = event.target.value
    let xhr = new XMLHttpRequest();
    xhr.open("GET",`/posts/like_post/${post_id}`)
    xhr.onreadystatechange = function(){
        if(xhr.status == 201 && xhr.readyState==4){
            likes = document.getElementById(post_id).innerText
            likes = parseInt(likes)
            likes += 1 
            document.getElementById(post_id).innerText = likes
            event.target.style.backgroundColor="blue"
        }
        else if(xhr.status==409 && xhr.readyState==4){
            likes = document.getElementById(post_id).innerText
            likes = parseInt(likes)
            likes -= 1
            document.getElementById(post_id).innerText = likes 
            event.target.style.backgroundColor="white"
        }
    }
    xhr.send()
}

function handleComment(event){
    post_id = parseInt(event.target.value)
    content = document.getElementById(`user-comment-field${post_id}`).value
    console.log(content)
    let xhr = new XMLHttpRequest()
    xhr.open("POST",`/posts/comment/${post_id}`)
    xhr.setRequestHeader('Content-Type', 'text/plain');
    xhr.send(content)

}