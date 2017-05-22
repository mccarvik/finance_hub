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
    var overlay = $("<div class='loader' id='loader'></div>");
    overlay.appendTo(document.body);
    $.ajax({
        type: 'POST',
        url: '/equity_analysis',
        data: {
        action: "get_data" },
        timeout: 60000 * 5,     // 5 minutes
        success: function()
        {
            console.log('Finished Retrieving Data');
            $('#loader').addClass("hide-loader");
            return;
        },
        error: function(xmlhttprequest, textstatus, message) {
            if(textstatus==="timeout") {
                alert("got timeout");
            } else {
                alert(message);
            }
        },
        complete: function()
        {
            console.log('Completed');
            return;
        },
        
    });
    
}

function eqanal_gen_charts(event, token) {
    console.log('Generating charts, sending them to Python backend');
}

