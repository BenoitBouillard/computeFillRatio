
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

    var franceRanking = new TableData("#franceRanking",
    {
        source: "gen/community_zones.json",
        post_source : function(data) {
            return data['France'].zones
        },
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
        row_id: function(data) { return data.name},
        highlight: "zone_statshunter",
        post_action_td: {
            name: function(td, data) {
                $(td).wrapInner('<a href="zone.html?country=France&zone='+data.name+'"></a>')
            }
        },
        post_action_tr: function(tr, data) {
        }
    })

    var belgiqueRanking = new TableData("#belgiqueRanking",
    {
        source: "gen/community_zones.json",
        post_source : function(data) {
            return data['Belgique'].zones
        },
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
        row_id: function(data) { return data.name},
        highlight: "zone_statshunter",
        post_action_td: {
            name: function(td, data) {
                $(td).wrapInner('<a href="zone.html?country=Belgique&zone='+data.name+'"></a>')
            }
        },
        post_action_tr: function(tr, data) {
        }
    })

    var suisseRanking = new TableData("#suisseRanking",
    {
        source: "gen/community_zones.json",
        post_source : function(data) {
            return data['Suisse'].zones
        },
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
        row_id: function(data) { return data.name},
        highlight: "zone_statshunter",
        post_action_td: {
            name: function(td, data) {
                $(td).wrapInner('<a href="zone.html?country=Suisse&zone='+data.name+'"></a>')
            }
        },
        post_action_tr: function(tr, data) {
        }
    })

    var allemagneRanking = new TableData("#allemagneRanking",
    {
        source: "gen/community_zones.json",
        post_source : function(data) {
            return data['Allemagne'].zones
        },
        fields: {
            ratio:  user => parseFloat((100.0*user["visited"]/user["size"]).toFixed(2)),
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
        row_id: function(data) { return data.name},
        highlight: "zone_statshunter",
        post_action_td: {
            name: function(td, data) {
                $(td).wrapInner('<a href="zone.html?country=Allemagne&zone='+data.name+'"></a>')
            }
        },
        post_action_tr: function(tr, data) {
        }
    })


})
