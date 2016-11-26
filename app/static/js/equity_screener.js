function run_screening(event, token) {
    var overlay = $('<div id="waiting"> </div>');
    overlay.appendTo(document.body)
    var filts = [];
    $("span.num_screen").each( function(index) {
        var t_val = $( this ).find('input').val()
        if (t_val != "") {
            var t_id = this.id;
            var t_cond = $( this ).find('select').val();
            var f = [t_id, t_cond, t_val];
            filts.push(f);
        };
    });
    filter_obj = {filts: filts}
    filts = JSON.stringify(filter_obj)
    console.log(filts)
    
    $.ajax({
        type: 'POST',
        url: '/equity_screener',
        data: {
            action: "run_screening",
            filters: filts
        },
        success: function()
        {
            console.log('Ran Screening')
        }
    });
}

function get_data(event, token) {
    var overlay = $('<div id="waiting"> </div>');
    overlay.appendTo(document.body)
    console.log('grabbing data - begin')
    $.ajax({
        type: 'POST',
        url: '/equity_screener',
        data: {
            action: "get_data" 
        },
        success: function()
        {
            console.log('Got Data')
        }
    });
}