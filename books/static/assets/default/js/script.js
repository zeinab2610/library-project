
window.uni_modal = function($title = '', $url = '', $size = "") {
    start_loader()
    $.ajax({
        url: $url,
        error: err => {
            console.log()
            alert("An error occured")
        },
        success: function(resp) {
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
window._conf = function($msg = '', $func = '', $params = []) {
    $('#confirm_modal #confirm').attr('onclick', $func + "(" + $params.join(',') + ")")
    $('#confirm_modal .modal-body').html($msg)
    $('#confirm_modal').modal('show')
}

$(function() {
    $('#user-form').submit(function(e) {
        e.preventDefault();
        var _this = $(this)
        $('.err-msg').remove();
        var el = $('<div>')
        el.addClass("alert alert-danger err-msg")
        el.hide()
        if (_this[0].checkValidity() == false) {
            _this[0].reportValidity();
            return false;
        }
        start_loader();
        console.log(new FormData($(this)[0]));
       
        $.ajax({
            headers: {
                "X-CSRFToken": '{{csrf_token}}'
            },
            url: '/save_user',
            data: new FormData($(this)[0]),
            cache: false,
            contentType: false,
            processData: false,
            method: 'POST',
            type: 'POST',
            dataType: 'json',
            error: err => {
                console.log(err)
                alert("An error occured", 'error');
                end_loader();
            },
            success: function(resp) {
                if (typeof resp == 'object' && resp.status == 'success') {
                    location.reload()
                } else if (resp.status == 'failed' && !!resp.msg) {
                    el.text(resp.msg)
                } else {
                    el.text("An error occured", 'error');
                    end_loader();
                    console.err(resp)
                }
                _this.prepend(el)
                el.show('slow')
                $("html, body, .modal").scrollTop(0);
                end_loader()
            }
        })
    })

    $('#category-form').submit(function(e) {
        console.log('here');
        e.preventDefault();
        var _this = $(this)
        $('.err-msg').remove();
        var el = $('<div>')
        el.addClass("alert alert-danger err-msg")
        el.hide()
        if (_this[0].checkValidity() == false) {
            _this[0].reportValidity();
            return false;
        }
        start_loader();
        $.ajax({
            headers: {
                "X-CSRFToken": '{{csrf_token}}'
            },
            url:   '/save_category',
            data: new FormData($(this)[0]),
            cache: false,
            contentType: false,
            processData: false,
            method: 'POST',
            type: 'POST',
            dataType: 'json',
            error: err => {
                console.log(err)
                alert("An error occured", 'error');
                end_loader();
            },
            success: function(resp) {
                if (typeof resp == 'object' && resp.status == 'success') {
                    location.reload()
                } else if (resp.status == 'failed' && !!resp.msg) {
                    el.text(resp.msg)
                } else {
                    el.text("An error occured", 'error');
                    end_loader();
                    console.err(resp)
                }
                _this.prepend(el)
                el.show('slow')
                $("html, body, .modal").scrollTop(0);
                end_loader()
            }
        })
    })

})





