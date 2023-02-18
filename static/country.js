
import {TableData} from "./libs/table_data.js?version=1.1"

$(document).ready(function(){

    var country_name = false;
    {
        const queryString = window.location.search
        const urlParams = new URLSearchParams(queryString);
        country_name = urlParams.get('country')
        if (country_name) {
            $('#countriesRanking').hide()
            $('span[data-replace="name"]').text(country_name)
            document.title = "[x] "+ country_name
        } else {
            $('#countryRanking').hide()
            $('#breadcrumb>li:last-child').remove()
        }
        $('#breadcrumb>li:last-child').addClass("active")
    }

    if (!country_name) {
        var countryRanking = new TableData("#countriesRanking",
        {
            source: "gen/community_zones.json",
            row_id: function(data) { return data.name},
            highlight: "country_statshunter",
            fields: {
                ratio:  zone => parseFloat((100.0*zone.all.visited/zone.all.size).toFixed(2))
            },
            post_action_td: {
                'name': function(td, data) {
                    $(td).wrapInner(`<a href="country.html?country=${data.name}"></a>`)
                }
            },
            post_action_tr: function(tr, data) {
            }
        })
    }

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
            },
            'user_1': function(td, data) {
                if (data.users.length >= 1) {
                    $(td).wrapInner(`<a target="_blank" href="map.html?title=${data.zone.name} pour ${data.users[0].user}&geojson=${data.users[0].geojson}"></a>`)
                }
            },
            'user_2': function(td, data) {
                if (data.users.length >= 2) {
                    $(td).wrapInner(`<a target="_blank" href="map.html?title=${data.zone.name} pour ${data.users[1].user}&geojson=${data.users[1].geojson}"></a>`)
                }
            },
            'user_3': function(td, data) {
                if (data.users.length >= 3) {
                    $(td).wrapInner(`<a target="_blank" href="map.html?title=${data.zone.name} pour ${data.users[2].user}&geojson=${data.users[2].geojson}"></a>`)
                }
            },
        },
        post_action_tr: function(tr, data) {
            $(`<td><a target="_blank" href="map.html?title=Communauté pour ${data.zone.name}&geojson=${data.geojson}">carte</a></td>`).appendTo(tr)
        }
    }

    if (country_name) {
        var franceRanking = new TableData("#countryRanking", Object.assign({}, config_base, {
            country: country_name
        }))
    }

})
