$(document).ready(function () {
    console.log('h1')
    if (window.jQuery) {  
        // jQuery is loaded
        console.log('jq')
    } else {
        // jQuery is not loaded
        console.log('no jq')
    }
});

function opt_vanilla_calc_prem(event, token) {
    var overlay = $('<div id="waiting"> </div>');
    overlay.appendTo(document.body);
    var typ = "P";
    var und = $("#underlying_val").val();
    var k = $("#strike_val").val();
    var t = $("#tenor_val").val();
    var v = $("#vol_val").val();
    console.log('und:' + und);
    
    $.ajax({
        type: 'POST',
        url: '/option/vanilla',
        data: {
            action: "prem_calc",
            otype: typ,
            underlying: und,
            strike: k,
            tenor: t,
            vol: v
        },
        success: function()
        {
            console.log('Vanilla Option Calculation Prem')
        }
    });
}

function opt_vanilla_calc_vol(event, token) {
    var overlay = $('<div id="waiting"> </div>');
    overlay.appendTo(document.body);
    var typ = "P";
    var und = $("#underlying_val").val();
    var k = $("#strike_val").val();
    var t = $("#tenor_val").val();
    var p = $("#prem_val").val();
    
    $.ajax({
        type: 'POST',
        url: '/option/vanilla',
        data: {
            action: "vol_calc",
            otype: typ,
            underlying: und,
            strike: k,
            tenor: t,
            prem: p
        },
        success: function()
        {
            console.log('Vanilla Option Calculation Vol')
        }
    });
}