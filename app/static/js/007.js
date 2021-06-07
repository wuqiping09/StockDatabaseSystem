// js by 007肝死队

$(function() {
    var ipost = $("#ipost");
    var icomment = $("#icomment");
    var inotification = $("#inotification");
    countInputNum(ipost.find("textarea"), ipost.find("#iwcnt"), ipost.find("#iwmax"));
    disableEnter(ipost.find("textarea"), ipost.find("#iwmax"));
    countInputNum(icomment.find("textarea"), icomment.find("#iwcnt"), icomment.find("#iwmax"));
    disableEnter(icomment.find("textarea"), icomment.find("#iwmax"));
    countInputNum(inotification.find("textarea"), inotification.find("#iwcnt"), inotification.find("#iwmax"));
    disableEnter(inotification.find("textarea"), inotification.find("#iwmax"));
});

// by pl
function countInputNum(textArea, numItem, maxNum){
    textArea.on('input propertychange', function(){
        numItem.text($(this).val().length);
    });
}

function disableEnter(textArea, maxNum){
    textArea.keydown(function (e){
        if($(this).val().length >= maxNum.text()){
            var key = $(this).event ? e.keyCode : e.which;
            if(key.toString() === "13"){
                return false;
            }
        }
    });
}

// by wgd
function bbs_reply(pos) {
    var rpl_body = document.getElementById("comment-"+pos);
    if(rpl_body){
        var comment_replied = document.getElementById("replied");
        var comment_replied_pos = document.getElementById("replied_pos");
        var comment_replied_body = document.getElementById("replied_body");
        var comment_body = document.getElementById("comment");
        var form_value = document.getElementById("comment_replied_pos")
        comment_replied.style.display = "block";
        comment_replied_pos.innerHTML = "回复 " + pos + " 楼的评论：";
        comment_replied_body.innerHTML = rpl_body.innerHTML;
        comment_body.value = "@ " + pos + " 楼：";
        form_value.value = pos;
    }
}

function reply_cancel() {
    var comment_replied = document.getElementById("replied");
    var comment_body = document.getElementById("comment");
    var form_value = document.getElementById("comment_replied_pos")
    comment_replied.style.display = "none";
    comment_body.value = "";
    form_value.value = 0;
}