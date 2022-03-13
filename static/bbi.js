import {TableData} from "./libs/table_data.js?version=1.1"

$(document).ready(function(){

    var bbi_ranking = new TableData("#ranking_table",
    {
        source: "gen/bbi.json",
        row_id: function(data) { return data.name},
        highlight: "user_statshunter",
        fields: {
        },
        post_action_td: {
            'name': function(td, data) {
                $(td).wrapInner('<a href="user.html?user='+data.name+'"></a>')
            }
        },
        post_action_tr: function(tr, data) {
        }
    })


    $('#copyToClipboard').click(function() {
        console.log("copyToClipboard")
        result = "Classement BBI "
        result += " trié par " + $('th[data-sort][data-sorted="true').data("text") + ":\n"
        $('tr.kikou').each(function() {
            result += $("td:eq(0)", this).text() + ") " + $("td:eq(1)", this).text()
            result += " : " + $("td:eq(2)", this).text()
            result += " / " + $("td:eq(3)", this).text()
            result += " / " + $("td:eq(4)", this).text()
            result += " / " + $("td:eq(5)", this).text()
            result += " / " + $("td:eq(6)", this).text()
            result += " = " + $("td:eq(7)", this).text()
            result +="\n"
        })

        navigator.clipboard.writeText(result).then(function() {
          window.alert("Le classement est copié dans le presse papier")
        }, function(err) {
          window.alert("Un problème est arrivé:"+ err.message)
        });
        console.log(result)
    })



})
