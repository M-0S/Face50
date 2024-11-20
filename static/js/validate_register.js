var username = document.getElementById("username");
var password = document.getElementById("password");
var confirmation = document.getElementById("confirmation");
var submitBtn = document.getElementById("submitBtn");

function validateRegister(submit=false) {
    if (username.value.length < 3) {
        return username.setCustomValidity("Usernames can be 3 to 20 characters long.");
    } else if (!/^[a-zA-Z0-9._]+$/.test(username.value)) {
        return username.setCustomValidity("Usernames may only contain letters, numbers, and _.");
    } else if (!/^(?=^[^_]+_?[^_]+$)/.test(username.value)) {
        return username.setCustomValidity("Usernames can have at most one _, but not start nor end with it.");
    } else if (!/^(?!^\d+$)/.test(username.value)) {
        return username.setCustomValidity("Usernames cannot be all numbers.");
    } else {
        username.setCustomValidity('');
    }

    if (password.value.length < 8) {
        return password.setCustomValidity('Passwords must be between 8 and 20 characters long.');
    } else if (/\s/g.test(password.value)) {
        return password.setCustomValidity('Passwords cannot contain spaces.');
    } else {
        password.setCustomValidity('');
    }

    if (password.value != confirmation.value) {
        return confirmation.setCustomValidity("Passwords don't match.");
    } else {
        confirmation.setCustomValidity('');
    }

    if (submit == true) {
        submitBtn.classList.add('disabled');
        submitBtn.innerHTML='Signing Up...';
    }
}

username.onkeyup = validateRegister;
password.onkeyup = validateRegister;
confirmation.onkeyup = validateRegister;
