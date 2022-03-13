import {TableData} from "./libs/table_data.js?version=1.1"

$(document).ready(function(){


    // ############ USER NAME ############
    var user_name = false;
    {
        const queryString = window.location.search
        const urlParams = new URLSearchParams(queryString);
        user_name = urlParams.get('user')
        $('span[data-replace="name"]').text(user_name)
        document.title = "[x] "+ user_name
        $("#user_map_link").attr("href", "map.html?user="+user_name)
    }

    var table = new TableData("#ranking_table",
    {
        source: "gen/users.json",
        post_source : function(data) {
            return data[user_name].zones
        },

        row_id: function(data) { return data.name},
        highlight: "zone_statshunter",
        fields: {
            ratio:  user => parseFloat((100.0*user["visited"]/user["total"]).toFixed(2))
        },
        post_action_td: {
            'zone': function(td, data) {
                $(td).wrapInner('<a target="_blank" href="map.html?user='+user_name+'"&zone='+data.name+'></a>')
            }
        },
        post_action_tr: function(tr, data) {
        }
    })


})
