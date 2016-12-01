function fut_calc(event, token) {
    var overlay = $('<div id="waiting"> </div>');
    overlay.appendTo(document.body);
    // var vol_prem = ""
    // $("input:radio[name=calc]").click(function() {
    //    vol_prem = $(this).val();
    // });
    var typ = $('input[name=calc]:checked').val();
    var und = $("#underlying").val();
    var ir = $("#ir_val").val();
    var inc_yld = $("#inc_yld").val();
    var conv_yld = $("#conv_yld").val();
    var cst_cry = $("#cst_cry").val();
    var tenor = $("#tenor").val();
    var price = $("#price").val();
    
    $.ajax({
        type: 'POST',
        url: '/futures_calc',
        data: {
            action: "fut_calc",
            fut_for: typ,
            und: und,
            ir: ir,
            inc_yld: inc_yld,
            conv_yld: conv_yld,
            cst_cry: cst_cry,
            tenor: tenor,
            price: price
        },
        success: function()
        {
            console.log('Futures Calculation')
        }
    });
}