(function () {
    $('.delete-pic-button').click(function (event) {
        event.preventDefault();
        event.stopPropagation();
        that = this;
        var jqxhr = $.ajax({
            url: event.currentTarget.href,
            method: 'DELETE'
        }).done(function (response) {
            if (response.changed_main) {
                $('#main_pic_' + response.old_main_id).parent().remove();
                var new_main_pic = $('#pic_' + response.new_main_id);
                new_main_pic
                    .attr('id', 'main_pic_' + response.new_main_id);
                var parent = new_main_pic.parent();
                parent.removeClass('all-pictures');
                parent.prependTo('.picture-box');
            } else {
                $(that).parent().remove();
            }
        }).fail(function () {
            alert("error");
        });
    })
})();