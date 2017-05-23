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
        success: function()
        {
            console.log('Finished Retrieving Data');
            $('#loader').addClass("hide-loader");
        },
        error: function(xmlhttprequest, textstatus, message) {
            // if(textstatus==="timeout") {
            //     alert("got timeout");
            // } else {
            //     alert(textstatus);
            // }
            console.log('Errored out, still not sure why, loading' +
                        ' DB may take a few more minutes');
            $('#loader').addClass("hide-loader");
        },
    });
}

function eqanal_gen_charts(event, token) {
    ticker = $('#eqanal_ticker').val()
    date = $('#eqanal_date').val()
    chart = $('#eqanal_charts').val()
    chart_data = {
        d : date,
        c : chart,
        t : ticker
    }
    console.log('Generating charts, sending them to Python backend');
    var overlay = $("<div class='loader' id='loader'></div>");
    overlay.appendTo(document.body);
    $.ajax({
        type: 'POST',
        url: '/equity_analysis',
        data: {
            action: "gen_charts",
            data: JSON.stringify(chart_data)
        },
        success: function()
        {
            console.log('Finished Retrieving Data');
            $('#loader').addClass("hide-loader");
        },
        error: function(xmlhttprequest, textstatus, message) {
            // if(textstatus==="timeout") {
            //     alert("got timeout");
            // } else {
            //     alert(textstatus);
            // }
            console.log('Errored out, still not sure why, loading' +
                        ' DB may take a few more minutes');
            $('#loader').addClass("hide-loader");
        },
    });
}

