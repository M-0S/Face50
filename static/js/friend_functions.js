var changeDOM = true;
const friendsCount = document.getElementById('friendsCount');
const friendBtn = document.getElementById('friend');
const cancelBtn = document.getElementById('cancel');
const acceptRemoveBtns = document.getElementById('accept-remove');
const unfriendBtn = document.getElementById('unfriend');

if (window.location.pathname != '/profile') changeDOM = false;

function refreshPage(type) {
    if (window.location.pathname == '/friends') {
        window.location.replace(window.location.origin + `/friends?type=${type}`);
    }
}

function friend_request(user_id) {
    fetch("/friend_request", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({'user_id': user_id})
    });

    if (changeDOM) {
        friendBtn.classList.add('d-none');
        cancelBtn.classList.remove('d-none');
    };
}

function cancel_request(user_id) {
    fetch("/cancel_request", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({'user_id': user_id})
    }).then(res => refreshPage('sent'));

    if (changeDOM) {
        cancelBtn.classList.add('d-none');
        friendBtn.classList.remove('d-none');
    };
}

function accept_friend(user_id) {
    fetch("/accept_friend", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({'user_id': user_id})
    }).then(res => refreshPage('requests'));

    if (changeDOM) {
        acceptRemoveBtns.classList.add('d-none');
        unfriendBtn.classList.remove('d-none');
        friendsCount.innerHTML = parseInt(friendsCount.innerHTML) + 1;
    }
}

function remove_request(user_id) {
    fetch("/remove_request", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({'user_id': user_id})
    }).then(res => refreshPage('requests'));

    if (changeDOM) {
        acceptRemoveBtns.classList.add('d-none');
        friendBtn.classList.remove('d-none');
    }
}

function unfriend(user_id) {
    fetch("/unfriend", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({'user_id': user_id})
    }).then(res => refreshPage('friends'));

    if (changeDOM) {
        unfriendBtn.classList.add('d-none');
        friendBtn.classList.remove('d-none');
        friendsCount.innerHTML = parseInt(friendsCount.innerHTML) - 1;
    }
}
