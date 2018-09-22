$('#collapse1').on('show.bs.collapse', function () {
    $("#setup-menu-icon").removeClass("glyphicon-chevron-left");
    $("#setup-menu-icon").addClass("glyphicon-chevron-down");
});


$('#collapse1').on('hide.bs.collapse', function () {
    $("#setup-menu-icon").removeClass("glyphicon-chevron-down");
    $("#setup-menu-icon").addClass("glyphicon-chevron-left");
});


$(function () {
    if (window.location.pathname === "/cmdb/user_manager") {
        $("#systemSetting").addClass("in");
        $("#setup-menu-icon").toggleClass("glyphicon-chevron-down");
    }
});

