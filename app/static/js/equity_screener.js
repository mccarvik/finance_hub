function update_grid(data, id) {
    console.log("got here")
    var source =
    {
        localdata: data,
        datatype: "array"
    };
    var dataAdapter = new $.jqx.dataAdapter(source, {
        loadComplete: function (data) { },
        loadError: function (xhr, status, error) { }    
    });
    $("#jqxgrid").jqxGrid(
    {
        source: dataAdapter,
        columns: [
            { text: 'First Name', datafield: 'firstname', width: 100 },
            { text: 'Last Name', datafield: 'lastname', width: 100 },
            { text: 'Product', datafield: 'productname', width: 180 },
            { text: 'Quantity', datafield: 'quantity', width: 80, cellsalign: 'right' },
            { text: 'Unit Price', datafield: 'price', width: 90, cellsalign: 'right', cellsformat: 'c2' },
            { text: 'Total', datafield: 'total', width: 100, cellsalign: 'right', cellsformat: 'c2' }
        ]
    });
}

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
            return;
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