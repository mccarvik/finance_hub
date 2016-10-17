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
            console.log('Ran Screening')
        }
    });
}

function get_data(event, token) {
    var overlay = $('<div id="waiting"> </div>');
    overlay.appendTo(document.body)
    $.ajax({
        type: 'POST',
        url: '/equity_screener',
        data: {
        action: "get_data" },
        success: function()
        {
            console.log('Got Data')
        }
    });
}