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
    }

    var table = new TableData("#ranking_table",
    {
        source: "gen/users.json",
        post_source : function(data) {
            $("#user_map_link").attr("href", `map.html?title=${user_name}&geojson=${data[user_name].geojson}`)
            return data[user_name].zones
        },

        row_id: function(data) { return data.zone.code},
        highlight: "zone_statshunter",
        fields: {
            ratio:  user => parseFloat((100.0*user["visited"]/user["total"]).toFixed(2))
        },
        post_action_td: {
        },
        post_action_tr: function(tr, data) {
            $(`<td><a target="_blank" href="map.html?title=${user_name}&geojson=${data.geojson}">carte</a></td>`).appendTo(tr)
        }
    })


})
