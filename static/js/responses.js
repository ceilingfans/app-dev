function getBotResponse(input) {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: '/get_bard',
            type: 'POST',
            data: JSON.stringify({ input: input }),
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            success: function(data) {
                console.log(data.response);
                resolve(data.response);
            },
            error: function(error) {
                reject(error);
            }
        });
    });
}