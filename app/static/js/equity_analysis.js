$(document).ready(function () {
    if (window.jQuery) {  
        // jQuery is loaded
        console.log('jquery found')
    } else {
        // jQuery is not loaded
        console.log('no jquery')
    }
});

function eqanal_get_data(event, token) {
    console.log('Retrieving Data for all tickers in Member list and loading to DB\nNot just ticker entered');
    var overlay = $('<div id="waiting"> </div>');
    overlay.appendTo(document.body);
    $.ajax({
        type: 'POST',
        url: '/equity_analysis',
        data: {
        action: "get_data" },
        success: function()
        {
            console.log('Finished Retrieving Data');
        }
    });
}

function eqanal_gen_charts(event, token) {
    console.log('Generating charts, sending them to Python backend');
}

