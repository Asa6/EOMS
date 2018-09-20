$("#setup-menu").click(function () {
    // console.log("点击");
    // $("#setup-menu").addClass("active");
    $("#setup-menu-icon").toggleClass("glyphicon-chevron-down");
});

// $("#setup-menu").click(function () {
//     if ($("#systemSetting").hasClass("in")) {
//         // console.log("列表不存在");
//         var v = "no_in";
//         $.cookie('left_menu', v);
//         $("#setup-menu-icon").toggleClass("glyphicon-chevron-left");
//     }
//     else {
//         // console.log("列表存在");
//         var v = "in";
//         $.cookie('left_menu', v);
//         $("#setup-menu-icon").toggleClass("glyphicon-chevron-down");
//
//     }
//     // location.reload();
// });
//
// $(function () {
//     var v = $.cookie('left_menu');
//
//     if (v === "in") {
//
//         // $("#setup-menu-icon").toggleClass("glyphicon-chevron-down");
//         $("#systemSetting").addClass("in");
//         // $("#setup-menu").removeClass("collapsed");
//         $("#setup-menu-icon").toggleClass("glyphicon-chevron-down");
//
//     }
//     if (v === "no_in") {
//          // $("#setup-menu-icon").toggleClass("glyphicon-chevron-down");
//         $("#systemSetting").removeClass("in");
//         // $("#setup-menu").removeClass("collapsed");
//         $("#setup-menu-icon").addClass("glyphicon-chevron-left");
//     }
// });
$(function () {
    if (window.location.pathname === "/cmdb/user_manager"){
        $("#systemSetting").addClass("in");
        $("#setup-menu-icon").toggleClass("glyphicon-chevron-down");
    }
});