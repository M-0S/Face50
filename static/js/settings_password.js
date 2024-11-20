var new_password = document.getElementById("new_password");
var confirm_password = document.getElementById("confirm_password");
var updateBtn = document.getElementById("updateBtn");

function validatePassword(submit=false) {
    if (new_password.value.length < 8) {
        return new_password.setCustomValidity('Passwords must be between 8 and 20 characters long.');
    } else if (/\s/g.test(new_password.value)) {
        return new_password.setCustomValidity('Passwords cannot contain spaces.');
    } else {
        new_password.setCustomValidity('');
    }

    if (new_password.value != confirm_password.value) {
        return confirm_password.setCustomValidity("Passwords don't match.");
    } else {
        confirm_password.setCustomValidity('');
    }

    if (submit == true) {
        updateBtn.classList.add('disabled');
        updateBtn.innerHTML='Updating...';
    }
}

new_password.onkeyup = validatePassword;
confirm_password.onkeyup = validatePassword;
