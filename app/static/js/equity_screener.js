function update_grid(data) {
    var data = new Array();
    var firstNames =
    [
        "Andrew", "Nancy", "Shelley", "Regina", "Yoshi", "Antoni", "Mayumi", "Ian", "Peter", "Lars", "Petra", "Martin", "Sven", "Elio", "Beate", "Cheryl", "Michael", "Guylene"
    ];
    var lastNames =
    [
        "Fuller", "Davolio", "Burke", "Murphy", "Nagase", "Saavedra", "Ohno", "Devling", "Wilson", "Peterson", "Winkler", "Bein", "Petersen", "Rossi", "Vileid", "Saylor", "Bjorn", "Nodier"
    ];
    var productNames =
    [
        "Black Tea", "Green Tea", "Caffe Espresso", "Doubleshot Espresso", "Caffe Latte", "White Chocolate Mocha", "Cramel Latte", "Caffe Americano", "Cappuccino", "Espresso Truffle", "Espresso con Panna", "Peppermint Mocha Twist"
    ];
    var priceValues =
    [
        "2.25", "1.5", "3.0", "3.3", "4.5", "3.6", "3.8", "2.5", "5.0", "1.75", "3.25", "4.0"
    ];
    for (var i = 0; i < 1000; i++) {
        var row = {};
        var productindex = Math.floor(Math.random() * productNames.length);
        var price = parseFloat(priceValues[productindex]);
        var quantity = 1 + Math.round(Math.random() * 10);
        row["firstname"] = firstNames[Math.floor(Math.random() * firstNames.length)];
        row["lastname"] = lastNames[Math.floor(Math.random() * lastNames.length)];
        row["productname"] = productNames[productindex];
        row["price"] = price;
        row["quantity"] = quantity;
        row["total"] = price * quantity;
        data[i] = row;
    }
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


// function update_grid(d) {
//     console.log("got to grid")
//     data = JSON.parse(d)
//     console.log(data)
//     data_array = new Array()
//     for (i=0; i<data.length; i++) {
//         data_array[i] = data[i];
//     }
    
//     console.log(data_array)
//     var source = new $.jqx.dataAdapter({
//             localdata: data_array,
//             datatype: 'array',
//             datafields: data_array[0]})
//     console.log(source)
//     var options = {
//             source: source,
//             columns: data.columns,
//             width: '98%',
//             height: '98%',
//             filterable:true,
//             showfilterrow:true,
//             columnsresize: true,
//             selectionmode: 'multiplerows',
//     }
//     _options = $.extend( {}, options );
//     $( '#jqxgrid' ).jqxGrid( _options );
//     // $( '#jqxgrid' ).jqxGrid( 'expandallgroups' );
// }


function run_screening(event, num_screen_vals) {
    var overlay = $('<div id="waiting"> </div>');
    overlay.appendTo(document.body);
    var filts = [];
    $("span.num_screen").each( function(index) {
        var t_val = $( this ).find('input').val();
        if (t_val != "") {
            var t_id = $( this ).find('select.num_screen_opts').val();
            // var t_id = this.id;
            var t_cond = $( this ).find('select.num_screen_conds').val();
            var f = [t_id, t_cond, t_val];
            filts.push(f);
        };
    });
    filter_obj = {filts: filts};
    filts = JSON.stringify(filter_obj);
    console.log(filts);
    console.log("RUNNING SCREENING")
    
    $.ajax({
        type: 'POST',
        url: '/equity_screener',
        data: {
            action: "run_screening",
            filters: filts
        },
        success: function(results)
        {
            console.log('Ran Screening');
            update_grid(results);
            return;
        },
    });
}

function get_data(event) {
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

function add_filter(event, num_screen_vals) {
    var filters = "";
    num_screen_vals = dict_helper(num_screen_vals);
    for (i=0; i < num_screen_vals.length; i++) {
        filters = filters + "<option value='" + num_screen_vals[i] + "'>" + num_screen_vals[i] + "</option>\n";
    };
    $('div.num_screen').last().after("\
        <div class='num_screen'> \
            <span class='num_screen'> \
                <select class='num_screen_opts'>\n" +
                filters +
                "</select> \
                <select class='num_screen_conds'> \
                    <option value='='>=</option> \
                    <option value='<'><</option> \
                    <option value='>'>></option> \
                </select> \
                <input type='text' class='num_screen' value =''/> \
            </span> \
        </div>"
    );
};

function dict_helper(dict) {
    var i, arr = [];
    for(i in dict) {
        arr.push(dict[i]);
    };
    return arr;
};