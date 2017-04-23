function get_data(event, token) {
    var overlay = $('<div id="waiting"> </div>');
    overlay.appendTo(document.body)
    $.ajax({
        type: 'POST',
        url: '/tsy',
        data: {
        action: "get_data" },
        success: function()
        {
            console.log('Retrieving Treasury Bond Data')
        }
    });
}