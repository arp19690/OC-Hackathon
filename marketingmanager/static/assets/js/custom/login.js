function createCookie(name, value, days) {
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        var expires = "; expires=" + date.toGMTString();
    }
    else var expires = "";
    document.cookie = name + "=" + value + expires + "; path=/";
}

function readCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

function eraseCookie(name) {
    createCookie(name, "", -1);
}

//Auto-populating form if cookie exists
if (readCookie('oc_remember') == '1') {
    $('input[name="username"]').val(readCookie('oc_username'));
    $('input[name="password"]').val(readCookie('oc_password'));
    $('input[type="checkbox"]').prop("checked", true);
}

//When the user click on submit button, remember the login details
$('.login-btn').click(function (e) {
    e.preventDefault();
    if ($('input[type="checkbox"]').is(':checked')) {
        createCookie('oc_username', $('input[name="username"]').val());
        createCookie('oc_password', $('input[name="password"]').val());
        createCookie('oc_remember', '1');
    }
    else {
        eraseCookie('oc_username');
        eraseCookie('oc_password');
        eraseCookie('oc_remember');
    }
    $('form').submit();
});

//if enter pressed, submit the form
$('form').keydown(function (event) {
    var keyCode = (event.keyCode ? event.keyCode : event.which);
    if (keyCode == 13) {
        $('form').submit();
    }
});