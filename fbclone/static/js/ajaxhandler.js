

function handleClick(event){
    post_id = event.target.value
    console.log(post_id)
    let xhr = new XMLHttpRequest();
    xhr.open("GET",`/posts/like_post/${post_id}`)
    xhr.onreadystatechange = function(){
        likes = document.getElementById(`likes_count${post_id}`).innerText.split(" ")
        likes = parseInt(likes)
        if(xhr.status == 201 && xhr.readyState==4){
            likes += 1 
            document.getElementById(`likes_count${post_id}`).innerText = likes+" Likes"
            event.target.style.backgroundColor="blue"
        }
        else if(xhr.status==409 && xhr.readyState==4){
            likes -= 1
            document.getElementById(`likes_count${post_id}`).innerText = likes+" Likes" 
            event.target.style.backgroundColor="#0d6efd"
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
    userCommentField = document.getElementById(`user-comment-field${postId}`)
    userCommentField.setAttribute("data-parent-id",parentId)
    userCommentField.setAttribute("data-post-id",postId)

    let xhr = new XMLHttpRequest()
    xhr.open("GET", `/posts/commentauthorinfo/${parentId}`)
    xhr.onload = function(){
        if(xhr.status==200){
            authorInfo = JSON.parse(xhr.responseText)
            userCommentField.value = `@${authorInfo["first_name"]}\n`
            userCommentField.focus()
        }
    }
    xhr.send()
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
            if(parentId != 9999){
                document.getElementById(`replies${parentId}`).appendChild(comment)
            }
            else{
                document.getElementById(`comments${postId}`).appendChild(comment)
            }
            
            document.getElementById(`user-comment-field${postId}`).value = ''
            userCommentField = document.getElementById(`user-comment-field${postId}`)
            userCommentField.removeAttribute('data-parent-id')
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


function handleReadMore(event){
    postId = event.target.dataset.postid
    console.log(postId) 
    hiddenBody = document.getElementById(`hidden-body${postId}`)
    hiddenBody.style.display="inline"
    readLessLink = document.getElementById(`read-less-link${postId}`)
    readLessLink.style.display="inline"
    readMoreLink = document.getElementById(`read-more-link${postId}`)
    readMoreLink.style.display="none"
}

function handleReadLess(event){
    postId = event.target.dataset.postid
    hiddenBody = document.getElementById(`hidden-body${postId}`)
    hiddenBody.style.display="none"
    readLessLink = document.getElementById(`read-less-link${postId}`)
    readLessLink.style.display="none"
    readMoreLink = document.getElementById(`read-more-link${postId}`)
    readMoreLink.style.display="inline"
}

function handleStars(event){
    postId = event.target.dataset.postid
    csrfToken = document.getElementById(`csrftoken${postId}`).value
    console.log(document.getElementById(`quantity${postId}`).value)
    amount = parseInt(document.getElementById(`quantity${postId}`).value)
    let xhr = new XMLHttpRequest()
    xhr.open("POST", `/posts/star/${postId}/${amount}`)
    xhr.setRequestHeader('X-CSRFToken', csrfToken)
    xhr.setRequestHeader('Content-Type','text/plain')
    xhr.onload = function(){
        if(xhr.status == 201){
            response_json = JSON.parse(xhr.responseText)
            amount = parseInt(response_json.amount)
            alert(response_json.msg)
            stars = document.getElementById(`star-count${postId}`).innerText.split(" ")[1]
            stars = parseInt(stars)
            stars = stars + amount
            document.getElementById(`star-count${postId}`).innerText = `Stars: ${stars}`
        }
    } 
    xhr.send()
}