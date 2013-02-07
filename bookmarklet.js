
var a = $.get("//localhost:8080/bookmarklet")
$("body").before(a.responseText)
