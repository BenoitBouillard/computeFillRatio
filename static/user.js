$(document).ready(function(){

    // ############ USER NAME ############
    var user_name = false;
    {
        const queryString = window.location.search
        const urlParams = new URLSearchParams(queryString);
        user_name = urlParams.get('user')
        $('span[data-replace="name"]').text(user_name)
        document.title = "[x] "+ user_name
        $("#user_map_link").attr("href", "map.html?user="+user_name)
    }

    var ranking_data = null;

    function load_table() {
        var select = $('input[name="btnradio"]:checked').val()
        function get_val(user, item) {
            if (item=="ratio") {
                return parseFloat((100.0*user["visited"]/user["total"]).toFixed(2))
            }
            /*if (item=="last_activity") {
                return user['last_activity']
            }*/
            //if (select=="all") {
                return user[item]
            /*} else if (select=="standing") {
                return user['standing'][item]
            } else {
                return user[item] - user['history'][select][item]
            }*/
        }

        var max_field = {visited: null, square:null, total:null, ratio:null/*, last_activity:null*/ }
        $.each(ranking_data, function(name, user) {
            $.each(max_field, function(field, value) {
                if ($('th[data-field="'+field+'"]').data("sort")=="desc") {
                    if ((value == null) || (get_val(user, field) > value)) {
                        max_field[field] = get_val(user, field)
                    }
                } else {
                    if ((value == null) || (get_val(user, field) < value)) {
                        max_field[field] = get_val(user, field)
                    }
                }
            })
        })

        $.each(ranking_data, function(name, user) {
            if ($('tr[id="'+name+'"]').length) {
                tr = $('tr[id="'+user['name']+'"]')
                tr.children().not('td:first').remove()
            } else {
                tr = $('<tr class="kikou" id="'+user['name']+'"><td class="number">'+($('#ranking_table tr').length)+'</td></tr>').appendTo('#ranking_table')
                if (localStorage.getItem('highlight_user', null) == user['name']) {
                    tr.addClass("selected")
                }
            }
            var td = $('<td>' + user['name'] + '</td>').appendTo(tr)
            td.wrapInner('<a target="_blank" href="map.html?user='+user_name + "&zone="+name+'"></a>')
            $.each(max_field, function(field, max_value) {
                td = $('<td class="number">' + get_val(user, field) + '</td>').appendTo(tr)
                if (get_val(user, field) == max_value) td.addClass('max')
                if ((field=='last_activity') && (user['last_activity_url'] != "")) {
                    td.wrapInner('<a target="_blank" href="'+user['last_activity_url']+'"></a>')
                }
            })
            /*var td = $('<td></td>').appendTo(tr)
                td.append('<a href="user.html?user='+ user['name'] +'">detail</a>')
            if (user['kml_url']) {
                td.append('<a href="'+ user['kml_url'] +'" target="_blank"><img src="media/kml.png"></a>')
            }
            if (user['squadrats_url'] != "") {
                td.append('<span class="spacer"></span><a href="'+ user['squadrats_url'] +'" target="_blank"><img src="https://squadrats.com/squadrats-iconfav.png"></a>')
            }*/
        })
    }

    $('input[type=radio][name=btnradio]').change(function() {
      console.log($('input[name="btnradio"]:checked').val())
      $("th.trophy").data("sort", $('input[name="btnradio"]:checked').data('sort'))
      load_table();
      sort_table($('th[data-sort][data-sorted="true').index())
    });


    $.ajax("gen/users.json", {
      dataType: "json",
      cache: false,
      success: function(data) {
        ranking_data = data[user_name].zones
        load_table()
        sort_table($('th[data-sort][data-sorted="true').index())
      }
    })

    $('th[data-sort]').click(function(){
        $('th[data-sort][data-sorted="true').attr("data-sorted", "false")
        $(this).attr("data-sorted", "true")
        sort_table($(this).index())
    })

    function sort_table(index=1) {
        var table = $('#ranking_table')
        var rows = table.find('tr:gt(0)').toArray().sort(comparer(index))
        var thi = table.find('th').eq(index)
        var asc = 0
        if ($(thi).data("sort") == "asc") {
            asc = 1
        }

        if (!asc){rows = rows.reverse()}
        for (var i = 0; i < rows.length; i++){
            table.append(rows[i])
            $(rows[i]).find('td:first-child').html(i+1)
        }
    }

    function comparer(index) {
        return function(a, b) {
            var valA = getCellValue(a, index), valB = getCellValue(b, index)
            if (valA == valB) {
                var i2 = index==2?3:2
                valA = getCellValue(a, i2)
                valB = getCellValue(b, i2)
            }
            return $.isNumeric(valA) && $.isNumeric(valB) ? valA - valB : valA.toString().localeCompare(valB)
        }
    }
    function getCellValue(row, index){ return $(row).children('td').eq(index).text() }

    $('#copyToClipboard').click(function() {
        console.log("copyToClipboard")
        result = "Classement "/*+ $('input[name="btnradio"]:checked').data("text")*/
        result += " trié par " + $('th[data-sort][data-sorted="true').data("text") + ":\n"
        $('tr.kikou').each(function() {
            result += $("td:eq(0)", this).text() + ") " + $("td:eq(1)", this).text()
            result += " : " + $("td:eq(2)", this).text()
            result += " / " + $("td:eq(3)", this).text()
            result += " / " + $("td:eq(4)", this).text()
            result +="\n"
        })
        navigator.clipboard.writeText(result).then(function() {
          window.alert("Le classement est copié dans le presse papier")
        }, function(err) {
          window.alert("Un problème est arrivé:"+ err.message)
        });
        console.log(result)
    })


    $('#copy_ranking').click(async function() {
        async function get_blob_ranking() {
            const rep = await fetch("gen/ranking.bbcode")
            const bbcode = await rep.text()
            return new Blob([bbcode], { type: 'text/plain' })
        }

        async function copy_ranking() {
            if ( navigator.clipboard.write && !navigator.userAgent.includes("Chrome")) {
                return navigator.clipboard.write([new ClipboardItem({ "text/plain": get_blob_ranking() })])
            } else {
                const blob = await get_blob_ranking()
                const txt = await blob.text()
                return navigator.clipboard.writeText(txt)
            }
        }

        copy_ranking().then(function() {
            window.alert("Le classement est copié dans le presse papier")
        }, function(err) {
            window.alert("Un problème est arrivé: "+ err.message)
            window.open("gen/ranking.bbcode.html",'_blank');
        });
    })

    var touchtime = 0;
    var currentTarget = null;
    $("table").on("click", 'tr', function(event) {
        if (event.currentTarget.id=="") return
        if (touchtime == 0) {
            // set first click
            touchtime = new Date().getTime();
            currentTarget = event.currentTarget
        } else {
            // compare first click to this click and see if they occurred within double click threshold
            if ((((new Date().getTime()) - touchtime) < 800) && currentTarget == event.currentTarget) {
                // double click occurred
                if (($('tr.selected').length>0) && ($('tr.selected')[0].id == event.currentTarget.id)) {
                    $('tr.selected').removeClass('selected')
                    localStorage.setItem('highlight_user', null)
                } else {
                    $('tr.selected').removeClass('selected')
                    localStorage.setItem('highlight_user', event.currentTarget.id)
                    $(event.currentTarget).addClass('selected')
                }
                touchtime = 0;
            } else {
                // not a double click so set as a new first click
                touchtime = new Date().getTime();
                currentTarget = event.currentTarget
            }
        }
    });

})
