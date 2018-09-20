$("#del_session").click(function () {
    $.ajax({
        url: "/cmdb/admin",
        type: "POST",
        data: {
            "_type": "del_session"
        },
        success: function (data) {
            var obj = JSON.parse(data);

            if (obj.type === "del_session") {
                if (obj.status) {
                    $.removeCookie('per_page_count');

                    location.reload();
                } else {
                    alert(obj.error);
                }
            }
        }
    })
});
