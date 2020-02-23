$(document).ready(function(){
    $('[data-toggle="popover"]').popover({
        sanitizeFn: function (content) {
            return content
        },
        placement : 'top',
        html : true,
        title : 'User Info <a href="#" class="close" data-dismiss="alert">&times;</a>',
        content : '<button  class="btn btn-danger" data-toggle="modal" data-target="#taskModal">Task</button><br>'+
            '<button  class="btn btn-warning" data-toggle="modal" data-target="#eventModal">Event</button>'

    });
});




