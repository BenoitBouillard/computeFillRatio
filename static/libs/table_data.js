function getDescendantProp(obj, desc) {
  var arr = desc.split('.');
  while (arr.length) {
    obj = obj[arr.shift()];
  }
  return obj;
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

export class TableData {
    constructor(table_element, conf) {
        this.table = $(table_element)
        this.conf = conf
        this.data = null
        this.loadData()
        this.highlight_click()
    }

    loadTable() {
        var tableObj = this
        function get_val(user, item) {
            if ('fields' in tableObj.conf && item in tableObj.conf.fields) {
                return tableObj.conf.fields[item](user)
            }
            return getDescendantProp(user, item)
        }

        //var max_field = {cluster: null, visited: null, square:null /*, last_activity:null*/ }
        var max_field = {}
        $('th.trophy', this.table).each(function() {
            max_field[$(this).data("field")] = null
        })

        $.each(this.data, function(name, user) {
            $.each(max_field, function(field, value) {
                if ($('th[data-field="'+field+'"]', tableObj.table).data("sort")=="desc") {
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

        $.each(this.data, function(name, user) {
            var tr
            var rowId = tableObj.conf.row_id(user)
            if ($('tr[id="'+rowId+'"]', tableObj.table).length) {
                tr = $('tr[id="'+rowId+'"]', tableObj.table)
                tr.children().not('td:first').remove()
            } else {
                tr = $('<tr class="kikou" id="'+rowId+'"><td class="number">'+($('tr', tableObj.table).length)+'</td></tr>').appendTo(tableObj.table)
                if (localStorage.getItem(tableObj.conf.highlight, null) == rowId) {
                    tr.addClass("selected")
                }
            }
            var td = $('<td>' + user['name'] + '</td>').appendTo(tr)

            $.each(max_field, function(field, max_value) {
                td = $('<td class="number">' + get_val(user, field) + '</td>').appendTo(tr)
                if (get_val(user, field) == max_value) td.addClass('max')
            })
            tableObj.table.find('th[data-post]').each(function() {
                tableObj.conf.post_action_td[$(this).data("post")](tr.find('td').eq($(this).index()), user)
            })
            tableObj.conf.post_action_tr(tr, user)
        })
    }

    loadData() {
        var tableObj = this
        $.ajax(this.conf.source, {
          dataType: "json",
          cache: false,
          success: function(data) {
            if ('post_source' in tableObj.conf) {
                tableObj.data = tableObj.conf.post_source(data)
            } else {
                tableObj.data = data
            }
            tableObj.loadTable()
            tableObj.sort_table($('th[data-sort][data-sorted="true"]', this.table).index())
          }
        })
        $('th[data-sort]', tableObj.table).click(function(){
            $('th[data-sort][data-sorted="true"]', tableObj.table).attr("data-sorted", "false")
            $(this).attr("data-sorted", "true")
            tableObj.sort_table($(this).index())
        })

    }
    sort_table(index=1) {
        var rows = this.table.find('tr:gt(0)').toArray().sort(comparer(index))
        var thi = this.table.find('th').eq(index)
        var asc = 0
        if ($(thi).data("sort") == "asc") {
            asc = 1
        }

        if (!asc){rows = rows.reverse()}
        for (var i = 0; i < rows.length; i++){
            this.table.append(rows[i])
            $(rows[i]).find('td:first-child').html(i+1)
        }
    }
    highlight_click() {
        var highlight = this.conf.highlight
        var table = this.table
        var touchtime = 0;
        var currentTarget = null;
        this.table.on("click", 'tr', function(event) {
            if (event.currentTarget.id=="") return
            if (touchtime == 0) {
                // set first click
                touchtime = new Date().getTime();
                currentTarget = event.currentTarget
            } else {
                // compare first click to this click and see if they occurred within double click threshold
                if ((((new Date().getTime()) - touchtime) < 800) && currentTarget == event.currentTarget) {
                    // double click occurred
                    if (($('tr.selected', table).length>0) && ($('tr.selected', table)[0].id == event.currentTarget.id)) {
                        $('tr.selected', table).removeClass('selected')
                        localStorage.setItem(highlight, null)
                    } else {
                        $('tr.selected', table).removeClass('selected')
                        localStorage.setItem(highlight, event.currentTarget.id)
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
    }
}
