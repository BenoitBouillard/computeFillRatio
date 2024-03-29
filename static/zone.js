
import {TableData} from "./libs/table_data.js?version=1.1"


$(document).ready(function(){

    var country = false;
    var zone = false;
    {
        const queryString = window.location.search
        const urlParams = new URLSearchParams(queryString);
        zone = urlParams.get('zone')
        country = urlParams.get('country')
        $('span[data-replace="country"]').text(country)

        $('*[data-replace-tag]').each(function(){
            var tag = $(this).data('replace-tag')
            $(this).attr(tag, $(this).attr(tag).replace("%country%", country))
        })

        document.title = "[x] "+ zone
    }

    var zoneRanking = new TableData("#zoneRanking",
    {
        source: "gen/community_zones.json",
        post_source : function(data) {
            $('span[data-replace="zone"]').text(data[country].zones[zone].zone.name)
            return data[country].zones[zone].users
        },
        row_id: function(data) { return data.user},
        highlight: "user_statshunter",
        fields: {
            ratio:  zone => parseFloat((100.0*zone["visited"]/zone["total"]).toFixed(2))
        },
        post_action_td: {
            user: function(td, data) {
                $(td).wrapInner(`<a href="user.html?user=${data.user}"></a>`)
            }
        },
        post_action_tr: function(tr, data) {
            $(`<td><a target="_blank" href="map.html?title=${data.zone.name} pour ${data.user}&geojson=${data.geojson}">carte</a></td>`).appendTo(tr)
        }

    })

})
