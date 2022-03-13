
import {TableData} from "./libs/table_data.js?version=1.1"


$(document).ready(function(){
    userRanking = new TableData("#userRanking",
    {
        source: "gen/users.json",
        row_id: function(data) { return data.name},
        highlight: "user_statshunter",
        post_action_td: {
            'name': function(td, data) {
                $(td).wrapInner('<a target="_blank" href="map.html?user='+data['name']+'"></a>')
            }
        },
        post_action_tr: function(tr, data) {
            $('<td><a href="user.html?user='+ data['name'] +'">detail</a></td>').appendTo(tr)
        }

    })

})
