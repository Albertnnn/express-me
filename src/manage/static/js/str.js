/**
 * string utils
 */
var str = 'a';

function is_blank(s) {
    var isNonblank_re = /\S/;
    return String(s).search(isNonblank_re) == -1
}

function is_email(s) {
    var re = /^([a-zA-Z0-9_.-])+@(([a-zA-Z0-9-])+.)+([a-zA-Z0-9]{2,4})+$/;
    return re.test(s);
}
