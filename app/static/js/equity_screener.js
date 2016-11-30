function update_grid(data) {
    data = JSON.parse(data)
    console.log(data)
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