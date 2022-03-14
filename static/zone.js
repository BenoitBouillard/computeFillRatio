
import {TableData} from "./libs/table_data.js?version=1.1"


$(document).ready(function(){

    var country = false;
    var zone = false;
    {
        const queryString = window.location.search
        const urlParams = new URLSearchParams(queryString);
        zone = urlParams.get('zone')
        country = urlParams.get('country')
        $('span[data-replace="zone"]').text(zone)
        $('span[data-replace="country"]').text(country)
        document.title = "[x] "+ zone
    }

    var zoneRanking = new TableData("#zoneRanking",
    {
        source: "gen/community_zones.json",
        post_source : function(data) {
            return data[country].zones[zone].users
        },
        row_id: function(data) { return data.user},
        highlight: "user_statshunter",
        post_action_td: {
            user: function(td, data) {
                $(td).wrapInner('<a href="user.html?user='+data.user+'"></a>')
            }
        },
        post_action_tr: function(tr, data) {
            $('<td><a target="_blank" href="map.html?user='+ data.user +'&zone='+data.zone+'">carte</a></td>').appendTo(tr)
        }

    })

})
