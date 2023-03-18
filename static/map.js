import {styles, consts} from "./libs/consts.js?version=1.5"

export function empty(elt) {
    while(elt.firstChild) elt.removeChild(elt.firstChild)
}
export function addLiveEventListener(el, eventName, selector, eventHandler) {
  const wrappedHandler = (e) => {
    if (!e.target) return;
    const el = e.target.closest(selector);
    if (el) {
      const newEvent = Object.create(e, {
        target: {
          value: el
        }
      });
      eventHandler.call(el, newEvent);
    }
  };
  el.addEventListener(eventName, wrappedHandler);
  return wrappedHandler;
}

// ############ MAP SIZE ############
{
    function resizeDz(){
        if ($('#content').length > 0) {
            var newDzHeight = document.documentElement.clientHeight
            newDzHeight -= $('#content').offset().top;
            newDzHeight -= ($('#content').outerHeight()-$('#content').height());
            newDzHeight -= 10;
            var minDzHeight = 300;
            if (newDzHeight > minDzHeight) {
                $('#content').height(newDzHeight);
            } else {
                $('#content').height(minDzHeight);
            };
        }
        return document.documentElement.clientHeight
    }

    $(document).ready(function(){
        resizeDz()
        setTimeout(function(){
            window.scrollTo(0, 0);
        }, 0);
    });
    $(window).resize(function(){resizeDz()});
}

$(document).ready(function(){

    // ############ PARAMS TITLE & GEOJSON ############
    var geojson_file = null
    var title = null
    {
        const queryString = window.location.search
        const urlParams = new URLSearchParams(queryString);
        geojson_file = urlParams.get('geojson')
        title = urlParams.get('title')
        document.title = "[x] carte "+title
        $("#title").html(title)
    }

    // ############ MAP ############
    var mymap = L.map('content', {zoomSnap: 0.5, zoomDelta:0.5, attributionControl: false});

    // Create panes to add layers on the right z-index
    $.each(consts.panes, function(i, pane) {
        mymap.createPane(pane.name);
        mymap.getPane(pane.name).style.zIndex = pane.zIndex;
    })

    // ############ SAVE MAP ZOOM & CENTER ############
    {
        mymap.setView(JSON.parse(localStorage.getItem("kik_map_center")) || [48.85, 2.35],
                      JSON.parse(localStorage.getItem("kik_map_zoom")) || 10);

        mymap.on("moveend", function() {
            localStorage.setItem("kik_map_zoom", JSON.stringify(mymap.getZoom()))
            localStorage.setItem("kik_map_center", JSON.stringify(mymap.getCenter()))
        });
    }

    // ############ MAP LAYERS ############
    {
        // TILES SOURCES
        var layers_name = []
        var tile_layers = {}

        function load_layers() {
            layers_name = []
            tile_layers = {}
            consts.baseLayers.forEach(layer => {
                layers_name.push(layer.name)
                tile_layers[layer.name] = L.tileLayer(layer.url, layer)
            })
        }
        load_layers();

        var active_layers = [...layers_name]

        var control_layer = L.control.layers({}, {}, {}).addTo(mymap);

        function refresh_layers() {
            control_layer.remove()
            control_layer = L.control.layers({}, {}, {}).addTo(mymap);
            var al = layers_name.filter(name => active_layers.includes(name))
            if (al.length==0) {
                al = [...layers_name]
            }
            al.forEach(layer_name => {
                control_layer.addBaseLayer(tile_layers[layer_name], layer_name)
            })
            if (!al.includes(localStorage.getItem("layer"))) {
                localStorage.setItem("layer", al[0])
            }
            tile_layers[localStorage.getItem("layer")].addTo(mymap);
        }

        refresh_layers();

        mymap.on("baselayerchange", function(event) {
            localStorage.setItem("layer", event.name)
        })
    }

    // ############ GRID ############
    {
        let grid_layer = new Map([["14", null]])
        let grid_level = "14"

        function display_grid_level(level, style) {
            let shouldLayerBeDisplayed = (mymap.getZoom() > level-5)
            if (shouldLayerBeDisplayed) {
                let segments = generateGridSegments(mymap, level, 5000);
                if (segments) {
                    let geojson_grid = lines2geojson(segments, level)
                    grid_layer.set(level, L.geoJSON(geojson_grid, style).addTo(mymap))
                    return true
                }
            }
            return false
        }

        function display_grid() {
            var style_index = 0
            // Remove actual grids
            grid_layer.forEach(function(layer, level) {
                if (layer) {
                    layer.remove()
                    grid_layer.set(level, null)
                }
            })
            // Create grids
            grid_layer.forEach(function(layer, level) {
                if ((grid_level==level) || grid_level=="both") {
                    if (display_grid_level(level, styles.grid)) {
                        style_index += 1
                    }
                }
            })
        }

        $('body').on("level_change", function(event, level) {
            grid_level = level
            display_grid()
        });

        mymap.on("moveend", display_grid);
        display_grid();
    }


    // ############ TILES ############
    {
        var geojson;

        styles.tiles.style = function(feature) {
            if (feature.properties.kind in styles.tiles)
                return styles.tiles[feature.properties.kind]
            else
                return styles.tiles["tiles"]
        }
        styles.tiles.onEachFeature = function(feature, layer) {
            if (feature.properties.kind=="sub-cluster") {
                layer.bindPopup("sous cluster: "+feature.properties.size+" carré(s)")
            }
            if (feature.properties.kind=="cluster") {
                layer.bindPopup("cluster: "+feature.properties.size+" carré(s)")
            }
            if (feature.properties.kind=="max_square") {
                layer.bindPopup("max square: "+feature.properties.size+"x"+feature.properties.size)
            }
            if (feature.properties.kind=="max_square_sub") {
                layer.bindPopup("sous max-square: "+feature.properties.size+"x"+feature.properties.size)
            }
            if (feature.properties.kind=="visited") {
                layer.bindPopup("visité: "+feature.properties.size+" carré(s)")
            }
        }

        function squadrats_display(data) {
            return L.geoJSON(data, styles.tiles).addTo(mymap)
        }

        function center() {
            var center_zone = geojson
            turf.featureEach(geojson, function (feature) {
                if ((feature.properties.kind=="cluster") && (feature.properties.size>0)) {
                    center_zone = feature
                }
            })
            var bbox = turf.bbox(center_zone)
            mymap.fitBounds([[bbox[1], bbox[0]], [bbox[3], bbox[2]]]);

        }

        // center on cluster when click on button
        $("#squadrats-center").on("click", function () {
            center()
        })

        function load_squadrats_tiles(level, cache="default") {
            fetch(geojson_file, {cache: cache})
            .then(response => response.json())
            .then(data => {
                geojson = data
                squadrats_display(geojson)
                center()

                const list_elt = document.getElementById("sub-cluster-list")
                empty(list_elt)
                for (const [index, feature] of data.features.entries()) {
                    let html = false
                    if ((feature.properties.kind=="sub-cluster") && (feature.properties.size>10)) {
                        html = `<li><a class="dropdown-item" href="#" data-index="${index}">sous-cluster ${feature.properties.size}</a></li>`
                    }
                    if (feature.properties.kind=="max_square_sub") {
                        html = `<li><a class="dropdown-item" href="#" data-index="${index}">sous-max-square ${feature.properties.size}x${feature.properties.size}</a></li>`
                    }
                    if (feature.properties.kind=="max_square") {
                        html = `<li><a class="dropdown-item" href="#" data-index="${index}">max-square ${feature.properties.size}x${feature.properties.size}</a></li>`
                    }
                    if (feature.properties.kind=="cluster") {
                        html = `<li><a class="dropdown-item" href="#" data-index="${index}">cluster ${feature.properties.size}</a></li>`
                    }
                    if (html) {
                      list_elt.insertAdjacentHTML('beforeend', html)
                    }
                }

            });
        }


        $("#reload").on("click", function() {
            load_squadrats_tiles($("#level").val(), "reload")
        })

        load_squadrats_tiles()
    }

    addLiveEventListener(document.getElementById("sub-cluster-list"), "click", "a", function() {
        let index = 1*this.dataset.index
        let feature = geojson.features[index]
        let bbox = turf.bbox(feature)
        mymap.fitBounds([[bbox[1], bbox[0]], [bbox[3], bbox[2]]]);
    });


})
