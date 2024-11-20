// Adapted from https://github.com/twbs/bootstrap/issues/36064

jQuery(document).ready(function($) {
    $('.toast').toast('show');

    setTimeout(function() {
        $('.toast').toast('hide');
    }, 5000);

    $('.toast').on('show.bs.toast', function() {
        // alert('The toast is about to be shown.');
        $('.progress-bar').attr('aria-valuenow', 100);
    });
    $('.toast').on('shown.bs.toast', function() {
        // alert('The toast is now fully shown.');
        $(".progress-bar").each(function(i) {
            // Todo: Create time variable from Toast
            var displayTime = $('.toast').attr('data-bs-delay');
            $(this).animate({
                width: $(this).attr('aria-valuenow') + '%'
            });
            $(this).css({
                webkittransition: 'width '+displayTime+'ms ease-in-out',
                moztransition: 'width '+displayTime+'ms ease-in-out',
                otransition: 'width '+displayTime+'ms ease-in-out',
                transition: 'width '+displayTime+'ms ease-in-out'
            });
        });


    });
    $('.toast').on('hidden.bs.toast', function() {
        // Reset progress bar back to zero, and clear inline style
        $('.progress-bar').attr('aria-valuenow', 0).removeAttr("style");

    });
    // Open links in new window (because Codepen)
    $('a[rel=external]').attr('target', '_blank');
});
