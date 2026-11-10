$(document).ready(function () {

    // Dropdown
    $(document).on('click', '.dropdown-menu', function (e) {
        e.stopPropagation();
    });

    // Radio buttons
    $('.js-check :radio').change(function () {
        var check_attr_name = $(this).attr('name');

        if ($(this).is(':checked')) {
            $('input[name="' + check_attr_name + '"]')
                .closest('.js-check')
                .removeClass('active');

            $(this).closest('.js-check').addClass('active');
        }
    });

    // Checkboxes
    $('.js-check :checkbox').change(function () {
        $(this).closest('.js-check')
            .toggleClass('active', $(this).is(':checked'));
    });

    // Bootstrap tooltip
    if ($('[data-toggle="tooltip"]').length > 0) {
        $('[data-toggle="tooltip"]').tooltip();
    }

    // Django message auto-hide
    setTimeout(function () {
        $('.register-toast-container .alert').fadeTo(800, 0, function () {
            $(this).slideUp(400, function () {
                $(this).remove();
            });
        });
    }, 3000);

});

function confirmRemove(event, element) {
    event.preventDefault();

    Swal.fire({
        title: 'Are you sure?',
        text: 'You want to remove this product from your cart?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Yes, Remove it!',
        cancelButtonText: 'No, Keep it',
        reverseButtons: true
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = element.href;
        }
    });

    return false;
}