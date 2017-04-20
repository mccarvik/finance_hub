function update_grid(d) {
    console.log("got to grid")
    var data = JSON.parse(d);
    var final_data = new Array();
    var labels = data.shift();
    var cols = data.shift();
    for (var i = 0; i < data.length; i++) {
        var row = {};
        for (var j = 0; j < cols.length; j++) {
            row[cols[j]] = data[i][j]    
        }
        final_data[i] = row
    }
    var source =
    {
        localdata: final_data,
        datatype: "array"
    };
    
    // var grid_cols = []
    // for (var i=0; i<cols.length; i++) {
    //     grid_cols[i] = { text: labels[i], datafield: cols[i], width: 100 }
    // }
    // console.log(grid_cols)
    console.log(final_data)
    
    var dataAdapter = new $.jqx.dataAdapter(source, {
        loadComplete: function (final_data) { },
        loadError: function (xhr, status, error) { }    
    });
    $("#jqxgrid").jqxGrid(
    {
        source: dataAdapter,
        // columns: grid_cols,
        columns: [
            { text: 'Ticker', datafield: 'ticker', width: 100 },
            // { text: 'First Name', datafield: 'firstname', width: 100 },
        ],
        width: '98%',
        height: '98%',
        filterable:true,
        sortable: true, 
        showfilterrow:true,
        columnsresize: true,
        selectionmode: 'multiplerows',
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
            return;
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