const postForm = document.getElementById("postForm");
const postText = postForm.getElementsByTagName("textarea")[0];
const postImage = postForm.getElementsByTagName("input")[0];
const postButton = postForm.getElementsByTagName("button")[1];

postButton.addEventListener("click", (e)=>{
    if (!postText.value.trim() && !postImage.value) {
        postButton.setCustomValidity("Please include text and/or image to post.");
    } else {
        postButton.setCustomValidity("");
        postButton.classList.add('disabled');
        postButton.innerHTML += 'ing...';
    }
});

postForm.addEventListener("submit", (e)=>{
    if (!postText.value && !postImage.value) {
        e.preventDefault();
    }
});
