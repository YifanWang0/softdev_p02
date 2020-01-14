$(document).ready(function(){
    $('[data-toggle="popover"]').popover({
        sanitizeFn: function (content) {
            return content
        },
        placement : 'top',
        html : true,
        title : 'User Info <a href="#" class="close" data-dismiss="alert">&times;</a>',
        content : '<button  class="btn btn-info" data-toggle="modal" data-target="#myModal1">Open Modal1</button><br>'+
            '<button  class="btn btn-primary" data-toggle="modal" data-target="#myModal2">Open Modal2</button>'

    });
});




