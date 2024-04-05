// static/script.js
// static/script.js
$(document).ready(function() {
    $('form').submit(function(e) {
        e.preventDefault();

        var formData = {
            url: $('#url').val(),
            scheduled_time: $('#scheduled_time').val()
        };

        $.ajax({
            type: 'POST',
            url: '/submit',
            data: formData,
            success: function(response) {
                console.log(response);
                location.reload();
            },
            error: function(error) {
                console.error(error.responseText);
            }
        });
    });
});
