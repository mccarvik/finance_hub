function bond_calc(event, token) {
    var overlay = $('<div id="waiting"> </div>');
    overlay.appendTo(document.body)
    $.ajax({
        type: 'POST',
        url: '/bond',
        data: {
        action: "bond_calc" },
        success: function()
        {
            console.log('Bond Calculation')
        }
    });
}