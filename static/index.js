
import {TableData} from "./libs/table_data.js?version=1.1"


$(document).ready(function(){
    var userRanking = new TableData("#userRanking",
    {
        source: "gen/users.json",
        row_id: function(data) { return data.user},
        highlight: "user_statshunter",
        post_action_td: {
            'user': function(td, data) {
                $(td).wrapInner(`<a href="user.html?user=${data.user}"></a>`)
            }
        },
        post_action_tr: function(tr, data) {
            $(`<td><a target="_blank" href="map.html?user=${data.user}">carte</a></td>`).appendTo(tr)
        }

    })

})
