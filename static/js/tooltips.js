// I copied this code from somewhere but I forgot to credit it ;-;

const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));

$(document).on('shown.bs.tooltip', function (e) {
    setTimeout(function () {
        $(e.target).tooltip('hide');
    }, 1800);
});
