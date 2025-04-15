

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

function handleComment(event,parentId){
    postId = event.target.dataset.id
    userCommentField = document.getElementById(`user-comment-field${postId}`)
    content = userCommentField.value
    parentId = userCommentField.dataset.parentId
    if (parentId == undefined){
            postCommentxhr(postId,9999,content)
    }
    else{
            postCommentxhr(postId,parentId,content)

    }
}


function createComment(info,content,postId){
    console.log(info)
    commentDiv = document.createElement("div")
    commentDiv.classList.add("comment")

    profileImageSpan = document.createElement("span")
    profileImageSpan.classList.add("profile_image")

    profileImg = document.createElement("img")
    profileImg.setAttribute("src",info["profile_picture"])

    profileImageSpan.appendChild(profileImg)

    commentDiv.appendChild(profileImageSpan)

    commentandauthorDiv = document.createElement("div")
    commentandauthorDiv.classList.add("commentandauthor")

    authorSpan = document.createElement("span")
    authorSpan.classList.add("author")
    authorSpan.innerText = info["first_name"]

    contentSpan = document.createElement("span")
    contentSpan.innerText = content

    replyLink = document.createElement("a")
    replyLink.setAttribute("href","#")
    replyLink.innerText = 'Reply'
    replyLink.addEventListener("click",handleNestedReply)
    // replyLink.setAttribute("data-id",info["comment_id"])
    replyLink.setAttribute("data-comment-id",info["comment_id"])
    replyLink.setAttribute("data-post-id",postId)

    repliesLink = document.createElement("a")
    repliesLink.setAttribute("href","#")
    repliesLink.innerText = "replies"
    repliesLink.addEventListener("click",loadNestedReplies)
    repliesLink.setAttribute("data-comment-id", info["comment_id"])
    repliesLink.setAttribute("data-post-id",postId)

    repliesDiv = document.createElement("div")
    repliesDiv.classList.add(`replies${info["comment_id"]}`)
    repliesDiv.setAttribute("id",`replies${info["comment_id"]}`)

    commentandauthorDiv.appendChild(authorSpan)
    commentandauthorDiv.appendChild(contentSpan)
    commentandauthorDiv.appendChild(replyLink)
    commentandauthorDiv.appendChild(repliesLink)
    commentDiv.appendChild(commentandauthorDiv)
    commentDiv.appendChild(repliesDiv)

    return commentDiv
}


function handleNestedReply(event){
    parentId = event.target.dataset.commentId
    postId = event.target.dataset.postId
    console.log(parentId)
    console.log(postId)
    userCommentField = document.getElementById(`user-comment-field${postId}`)
    userCommentField.setAttribute("data-parent-id",parentId)
    userCommentField.setAttribute("data-post-id",postId)
    userCommentField.value = '@\n'
    userCommentField.focus()
}



function postCommentxhr(postId,parentId,content){
    csrfToken = document.getElementById(`csrftoken${postId}`).value

    let xhr = new XMLHttpRequest()
    xhr.open("POST", `/posts/comment/${postId}/${parentId}`)
    xhr.setRequestHeader('X-CSRFToken', csrfToken)
    xhr.setRequestHeader('Content-Type','text/plain')
    xhr.onload = function(){
        if(xhr.status == 201){
            info = JSON.parse(xhr.responseText)
            comment = createComment(info,content,postId)
            document.getElementById(`comments${postId}`).appendChild(comment)
            document.getElementById(`user-comment-field${postId}`).value = ''
        }
    } 
    xhr.send(content)
}


function loadNestedReplies(event){
    parentId = event.target.dataset.commentId
    console.log(parentId)
    postId = event.target.dataset.postId
    let xhr = new XMLHttpRequest()
    xhr.open("GET", `/posts/comment/${postId}/${parentId}`)
    xhr.onload = function(){
        nested_comments = JSON.parse(xhr.responseText)
        for(let id in nested_comments){
            info={}
            info["profile_picture"] = nested_comments[id].profile_picture
            info["first_name"] = nested_comments[id].author_name
            info["comment_id"] = id
            commentDiv = createComment(info,nested_comments[id].content,postId)
            document.getElementById(`replies${parentId}`).appendChild(commentDiv)
        }
    }
    xhr.send()
}
