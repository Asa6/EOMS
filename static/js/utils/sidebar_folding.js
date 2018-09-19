$(document).ready(function () {
    $(".toggle-sidebar").click(function () {
        $("#sidebar").toggleClass("collapsed");
        $("#content").toggleClass("col-md-12 col-md-10 col-md-offset-0");
        return false;
    });
});
