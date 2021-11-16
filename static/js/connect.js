function ws_connect() {
    ws.onopen = function(msg) {
        ws.send(JSON.stringify({ "status": "login", "name": user.username, "avatar": user.avatar }))
    }
    ws.onmessage = function(msg) {
        let data = JSON.parse(msg.data)
        if (data.status == "online") {
            $(".chat-list").empty()
            $(".c-number").text(data.users.length - 1)
            data.users.map(res => {
                if (res.username != user.username) {
                    let user_html = '<li class="chat-list-item"><img src="' + res.avatar + '" alt="chat"><span class="chat-list-name">' + res.username + '</span></li>'
                    $(".chat-list").append(user_html)
                }
            })
        } else if (data.status == "chat") {
            let html = '<div class="message-wrapper"><img class="message-pp" src="' + data.data.avatar + '" alt="profile-pic"><div class="message-box-wrapper"><div class="message-box">' + data.data.msg + '</div><span>' + set_time(data.data.time) + '</span></div></div>'
            $(".chat-wrapper").append(html)
        }

    };
}

function ws_send() {
    let data = $("input[name='message']").val()
    let send_data = {
        status: "chat",
        from: user.username,
        to: to_user,
        data: {
            avatar: user.avatar,
            msg: data,
            time: new Date().getTime()
        }
    }
    ws.send(JSON.stringify(send_data))
    let html = '<div class="message-wrapper reverse"><img class="message-pp" src="static/image/user1.gif" alt="profile-pic"><div class="message-box-wrapper"><div class="message-box">' + send_data.data.msg + '</div><span>' + set_time(send_data.data.time) + '</span></div></div>'
    $(".chat-wrapper").append(html)
    $("input[name='message']").val("")
}

function set_time(time = +new Date()) {
    var date = new Date(time + 8 * 3600 * 1000);
    return date.toJSON().substr(0, 19).replace('T', ' ').replace(/-/g, '.');
};

function change_chat() {
    $(".chat-list").on("click", ".chat-list-item", function() {
        let all_child = $(".chat-list").children("li")
            //console.log(all_child)
        all_child.map(res => {
            if (all_child[res].classList.contains("active")) {
                $(all_child[res]).removeClass("active")
            }
        })
        to_user = $(this).children("span").text()
        $(this).addClass("active")
        $("#target_avatar").attr("src", $(this).children("img").attr("src"))
        $("#target_name").text($(this).children("span").text())

    })
};

function get_userinfo() {
    $.ajax({
        type: "GET",
        url: "/api/userinfo",
        data: {
            token: Cookies.get("token")
        },
        success: function(res) {
            console.log(res)
            $(".app-profile-box-name").empty()
            $(".app-profile-box-name").append(res.data.username)
            $("#my_avatar").attr("src", res.data.avatar)
        }
    })
}