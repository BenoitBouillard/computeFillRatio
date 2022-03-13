
import {TableData} from "./libs/table_data.js?version=1.1"

$(document).ready(function(){


    countryRanking = new TableData("#countryRanking",
    {
        source: "gen/community_zones.json",
        row_id: function(data) { return data.name},
        highlight: "country_statshunter",
        fields: {
            ratio:  zone => parseFloat((100.0*zone.all.visited/zone.all.size).toFixed(2))
        },
        post_action_td: {
        },
        post_action_tr: function(tr, data) {
        }
    })

    franceRanking = new TableData("#franceRanking",
    {
        source: "gen/community_zones.json",
        post_source : function(data) {
            return data['France'].zones
        },
        fields: {
            ratio:  zone => parseFloat((100.0*zone.visited/zone.size).toFixed(2))
        },
        row_id: function(data) { return data.name},
        highlight: "zone_statshunter",
        post_action_td: {
        },
        post_action_tr: function(tr, data) {
        }
    })

    belgiqueRanking = new TableData("#belgiqueRanking",
    {
        source: "gen/community_zones.json",
        post_source : function(data) {
            return data['Belgique'].zones
        },
        fields: {
            ratio:  zone => parseFloat((100.0*zone.visited/zone.size).toFixed(2))
        },
        row_id: function(data) { return data.name},
        highlight: "zone_statshunter",
        post_action_td: {
        },
        post_action_tr: function(tr, data) {
        }
    })

    suisseRanking = new TableData("#suisseRanking",
    {
        source: "gen/community_zones.json",
        post_source : function(data) {
            return data['Suisse'].zones
        },
        fields: {
            ratio:  zone => parseFloat((100.0*zone.visited/zone.size).toFixed(2))
        },
        row_id: function(data) { return data.name},
        highlight: "zone_statshunter",
        post_action_td: {
        },
        post_action_tr: function(tr, data) {
        }
    })

    allemagneRanking = new TableData("#allemagneRanking",
    {
        source: "gen/community_zones.json",
        post_source : function(data) {
            return data['Allemagne'].zones
        },
        fields: {
            ratio:  user => parseFloat((100.0*user["visited"]/user["size"]).toFixed(2))
        },
        row_id: function(data) { return data.name},
        highlight: "zone_statshunter",
        post_action_td: {
        },
        post_action_tr: function(tr, data) {
        }
    })


})
