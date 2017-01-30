$('#delete').click(function(){
    $('#delete-modal').modal('show');
})

$('#edit').click(function(){
    window.location.href
})

$('#delete-confirm').click(function(event){
    $.ajax({
        url: '/image/' + window.location.pathname.split('/').slice(-1)[0],
        type: 'DELETE',
        success: function(){
            window.location.href='/gallery/'
        }
    })
})