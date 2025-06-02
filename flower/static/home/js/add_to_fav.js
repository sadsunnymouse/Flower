$(document).ready(function() {
    $(document).on('click', '.favorite-btn', function(e) {
        e.preventDefault();
        const $button = $(this);
        const productId = $button.data('product-id');
        const $icon = $button.find('i');
        const csrftoken = $('meta[name="csrf-token"]').attr('content');

        $.ajax({
            url: `/favorites/toggle-favorite/${productId}/`,
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            dataType: 'json',
            data: {},
            success: function(data) {
                if (data.status === "added") {
                    $icon.removeClass('far').addClass('fas').css('color', 'red');
                } else if (data.status === "removed") {
                    $icon.removeClass('fas').addClass('far').css('color', '#ccc');
                }
            },
            error: function(xhr, status, error) {
                console.error("Error:", error);
            }
        });
    });
});
