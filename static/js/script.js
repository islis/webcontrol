$('.device-switch').click(function(){
    var deviceId = $(this).data('id');  // $(this).attr('data-id')
    var state = $(this).is(':checked');
    $.post('/device/set-state/', {
        'id': deviceId,
        'state': state ? 'ON' : 'OFF',
        'csrfmiddlewaretoken': document.csrf_token,
    }).done(function() {
        var $state = $('.device_state-' + deviceId);
        $state.text(state ? 'ON' : 'OFF');
    });
});