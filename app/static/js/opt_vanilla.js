function opt_vanilla_calc(event, token) {
    var overlay = $('<div id="waiting"> </div>');
    overlay.appendTo(document.body)
    $.ajax({
        type: 'POST',
        url: '/bond',
        data: {
        action: "opt_vanilla_calc" },
        success: function()
        {
            console.log('Vanilla Option Calculation')
        }
    });
}