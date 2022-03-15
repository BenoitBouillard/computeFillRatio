
import {TableData} from "./libs/table_data.js?version=1.1"

$(document).ready(function(){


    var countryRanking = new TableData("#countryRanking",
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

    var config_base = {
        source: "gen/community_zones.json",
        post_source : function(data, conf) {
            return data[conf.country].zones
        },
        row_id: function(data) { return data.zone.code},
        highlight: "zone_statshunter",
        fields: {
            ratio:  zone => parseFloat((100.0*zone.visited/zone.size).toFixed(2)),
            user_1: function(zone) {
                if (zone['users'].length >= 1) {
                    var user = zone.users[0]
                    return user.user+ " ("+parseFloat((100.0*user.visited/user.total).toFixed(2))+"%)"
                }
                return ""
            },
            user_2: function(zone) {
                if (zone['users'].length >= 2) {
                    var user = zone.users[1]
                    return user.user+ " ("+parseFloat((100.0*user.visited/user.total).toFixed(2))+"%)"
                }
                return ""
            },
            user_3: function(zone) {
                if (zone['users'].length >= 3) {
                    var user = zone.users[2]
                    return user.user+ " ("+parseFloat((100.0*user.visited/user.total).toFixed(2))+"%)"
                }
                return ""
            },
        },
        post_action_td: {
            'zone.name': function(td, data) {
                $(td).wrapInner(`<a href="zone.html?country=${data.zone.country}&zone=${data.zone.code}"></a>`)
            }
        },
        post_action_tr: function(tr, data) {
        }
    }


    var franceRanking = new TableData("#franceRanking", Object.assign({}, config_base, {
        country: "France"
    }))

    var belgiqueRanking = new TableData("#belgiqueRanking", Object.assign({}, config_base, {
        country: "Belgique"
    }))

    var suisseRanking = new TableData("#suisseRanking", Object.assign({}, config_base, {
        country: "Suisse"
    }))

    var allemagneRanking = new TableData("#allemagneRanking", Object.assign({}, config_base, {
        country: "Allemagne"
    }))


})
