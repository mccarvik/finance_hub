$(document).ready(function () {
    if (window.jQuery) {  
        // jQuery is loaded
        console.log('jquery found')
    } else {
        // jQuery is not loaded
        console.log('no jquery')
    }
});

function opt_vanilla_calc(event, token) {
    var overlay = $('<div id="waiting"> </div>');
    overlay.appendTo(document.body);
    // var vol_prem = ""
    // $("input:radio[name=calc]").click(function() {
    //    vol_prem = $(this).val();
    // });
    var vol_prem = $('input[name=calc]:checked').val();
    var typ = $("#call_put").val();
    var und = $("#underlying_val").val();
    var k = $("#strike_val").val();
    var t = $("#tenor_val").val();
    var v = $("#vol_val").val();
    var p = $("#prem_val").val();
    var d = $("#div_val").val();
    
    $.ajax({
        type: 'POST',
        url: '/option/vanilla',
        data: {
            action: "calc",
            calc_type: vol_prem,
            otype: typ,
            underlying: und,
            strike: k,
            tenor: t,
            div: d,
            vol: v,
            prem: p 
        },
        success: function()
        {
            console.log('Vanilla Option Calculation Prem')
        }
    });
}
