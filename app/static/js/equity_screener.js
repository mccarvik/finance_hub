function run_screening(event, token) {
    var overlay = $('<div id="waiting"> </div>');
    overlay.appendTo(document.body)
    $.ajax({
        type: 'POST',
        url: '/equity_screener',
        data: {
        action: "run_screening" },
        success: function()
        {
            console.log('here 3')
        }
    });
}