function like(button) {
    const likeStatus = button.getElementsByTagName('i')[0];
    var likeCount = button.getElementsByTagName('small')[0];

    if (likeStatus.classList.contains("bi-hand-thumbs-up-fill")) {
        likeStatus.classList.add("bi-hand-thumbs-up");
        likeStatus.classList.remove("bi-hand-thumbs-up-fill");
        likeCount.innerHTML = parseInt(likeCount.innerHTML) - 1;
    } else {
        likeStatus.classList.add("bi-hand-thumbs-up-fill");
        likeStatus.classList.remove("bi-hand-thumbs-up");
        likeCount.innerHTML = parseInt(likeCount.innerHTML) + 1;

    }

    fetch("/like", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({'post_id': button.getAttribute('data-bs-postId')})
    });
}
