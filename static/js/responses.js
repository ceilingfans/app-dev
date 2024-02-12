function getBotResponse(input) {
    $.ajax({
        url: '/get_bard',
        type: 'POST',
        data: JSON.stringify({ input: input }),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function(data) {
            return data.response
        }
    });
}