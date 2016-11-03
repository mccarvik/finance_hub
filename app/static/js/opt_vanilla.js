function opt_vanilla_calc_prem(event, token) {
    var overlay = $('<div id="waiting"> </div>');
    overlay.appendTo(document.body)
    $.ajax({
        type: 'POST',
        url: '/option/vanilla',
        data: {
        action: "prem_calc" },
        success: function()
        {
            console.log('Vanilla Option Calculation Prem')
        }
    });
}

function opt_vanilla_calc_vol(event, token) {
    var overlay = $('<div id="waiting"> </div>');
    overlay.appendTo(document.body)
    $.ajax({
        type: 'POST',
        url: '/option/vanilla',
        data: {
        action: "vol_calc" },
        success: function()
        {
            console.log('Vanilla Option Calculation Vol')
        }
    });
}