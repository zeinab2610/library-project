const loader = $('<div>')
loader.attr('id', 'pre-loader')
loader.html('<div class="lds-facebook"><div></div><div></div><div></div></div>')

window.start_loader = function () {
    $('body').removeClass('loading')
    if ($('#pre-loader').length > 0)
        $('#pre-loader').remove();
    $('body').append(loader)
    $('body').addClass('loading')
}
window.end_loader = function () {
    if ($('#pre-loader').length > 0)
        $('#pre-loader').remove();
    $('body').removeClass('loading')
}
window.uni_modal = function ($title = '', $url = '', $size = "") {
    start_loader()
    $.ajax({
        url: $url,
        error: err => {
            console.log()
            alert("An error occured")
        },
        success: function (resp) {
            if (resp) {
                $('#uni_modal .modal-title').html($title)
                $('#uni_modal .modal-body').html(resp)
                if ($size != '') {
                    $('#uni_modal .modal-dialog').addClass($size + '  modal-dialog-centered')
                } else {
                    $('#uni_modal .modal-dialog').removeAttr("class").addClass("modal-dialog modal-md modal-dialog-centered")
                }
                $('#uni_modal').modal({
                    backdrop: 'static',
                    keyboard: false,
                    focus: true
                })
                $('#uni_modal').modal('show')
                end_loader()
            }
        }
    })
}
window._conf = function ($msg = '', $func = '', $params = []) {
    $('#confirm_modal #confirm').attr('onclick', $func + "(" + $params.join(',') + ")")
    $('#confirm_modal .modal-body').html($msg)
    $('#confirm_modal').modal('show')
}

$(function () {

    $('#topNav .nav-link').each(function () {
        var current = '{{ request.get_full_path | urlencode }}'
        if (current == $(this).attr('href')) {
            $(this).parent().addClass('active')
        }
    })

    $('#viewer_modal').on('shown.modal.bs', function () {
        $('#zoom-value').val(100)
        $('#img-viewer img').css(
            'transform',
            'scale(1)'
        )

    })
    $('#zoom-plus').click(function () {
        var scale = parseFloat($('#zoom-value').val())
        if (scale >= 200) return false;
        scale += 10
        $('#zoom-value').val(scale)
        scale = scale / 100
        $('#img-viewer img').css(
            'transform',
            'scale(' + (scale) + ')'
        )
    })
    $('#zoom-minus').click(function () {
        var scale = parseFloat($('#zoom-value').val())
        if (scale <= 0) return false;
        scale -= 10
        $('#zoom-value').val(scale)
        scale = scale / 100
        $('#img-viewer img').css(
            'transform',
            'scale(' + (scale) + ')'
        )
    })

    $('#book-tbl').find('td, th').addClass('px-2 py-1 align-middle')
    $('#book-tbl').DataTable({
        columnDefs: [{
            orderable: false,
            targets: [2]
        }],
        lengthMenu: [
            [25, 50, 100, -1],
            [25, 50, 100, "All"]
        ]
    })

    $('.edit-data').click(function () {
        var url = $(this).data('url');
        // Redirect the user to the specified URL
        window.location.href = url;
    })

    $('.view-data-book').click(function () {
        uni_modal("<i class='fa fa-th-list'></i> Book Details", $(this).attr('data-url'))
    })

    $('.delete-data-book').click(function () {
        _conf("Are you sure to delete this Book?", 'delete_book', ["'" + $(this).attr('data-url') + "'"])
    })

    $('#category-tbl').find('td, th').addClass('px-2 py-1 align-middle')

    $('#category-tbl').DataTable({
        columnDefs: [{
            orderable: false,
            targets: [2]
        }],
        lengthMenu: [
            [25, 50, 100, -1],
            [25, 50, 100, "All"]
        ]
    })

    $('.view-data-category').click(function () {
        uni_modal("<i class='fa fa-th-list'></i> Category Details", $(this).attr('data-url'))
    })

    $('.delete-data-category').click(function () {
        _conf("Are you sure to delete this Category?", 'delete_category', ["'" + $(this).attr('data-url') + "'"])
    })

})

function delete_book(url) {

    var _this = $('#confirm_modal .modal-body')
    $('.err-msg').remove();
    var el = $('<div>')
    el.addClass("alert alert-danger err-msg")
    el.hide()
    start_loader()
    $.ajax({
        headers: {
            "X-CSRFToken": "{{csrf_token}}"
        },
        url: url,
        dataType: 'JSON',
        error: err => {
            console.log(err)
            alert("an error occurred.")
            end_loader()
        },
        success: function (resp) {
            if (resp.status == 'success') {
                location.reload()
            } else if (!!resp.msg) {
                el.html(resp.msg)
                _this.prepend(el)
                el.show()
            } else {
                el.html("An error occurred")
                _this.prepend(el)
                el.show()
            }
            end_loader()
        }

    })
}

function delete_category(url) {

    var _this = $('#confirm_modal .modal-body')
    $('.err-msg').remove();
    var el = $('<div>')
    el.addClass("alert alert-danger err-msg")
    el.hide()
    start_loader()
    $.ajax({
        headers: {
            "X-CSRFToken": "{{csrf_token}}"
        },
        url: url,
        dataType: 'JSON',
        error: err => {
            console.log(err)
            alert("an error occurred.")
            end_loader()
        },
        success: function (resp) {
            if (resp.status == 'success') {
                location.reload()
            } else if (!!resp.msg) {
                el.html(resp.msg)
                _this.prepend(el)
                el.show()
            } else {
                el.html("An error occurred")
                _this.prepend(el)
                el.show()
            }
            end_loader()
        }

    })
}