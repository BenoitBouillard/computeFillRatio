
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

    // ############ USER NAME ############



    // ############ MAP ############
    var mymap = L.map('content', {zoomSnap: 0.5, zoomDelta:0.5, attributionControl: false});

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
    var baseLayers =[
       {
            name: "OSM Fr",
            maxZoom: 19,
            attribution: false,
            url: 'https://{s}.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png'
        },
        {
            name: "IGN carte",
            url: 'https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET=PM&FORMAT={format}&LAYER={layer}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}',
            attribution: false,
            maxZoom: 19,
            apikey: 'choisirgeoportail',
            layer: 'GEOGRAPHICALGRIDSYSTEMS.PLANIGNV2',
            format: 'image/png',
            style: 'normal'
        },
        {
            name: "IGN Sat.",
            url: 'https://wxs.ign.fr/{apikey}/geoportail/wmts?service=WMTS&request=GetTile&version=1.0.0&tilematrixset=PM&tilematrix={z}&tilecol={x}&tilerow={y}&layer=ORTHOIMAGERY.ORTHOPHOTOS&format=image/jpeg&style=normal',
            attribution: false,
            maxZoom: 19,
            apikey: 'choisirgeoportail',
            format: 'image/jpeg',
            style: 'normal'
        },
        {
            name: "ESRI Sat.",
            url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attribution: false,
            maxZoom: 19
        },
        {
            name: "Google Sat.",
            url: 'http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
            subdomains:['mt0','mt1','mt2','mt3'],
            attribution: false,
            maxZoom: 20
        },
        {
            name: "Google Hybrid",
            url: 'http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}',
            subdomains:['mt0','mt1','mt2','mt3'],
            attribution: false,
            maxZoom: 20
        }
    ]


        // TILES SOURCES
        var layers_name = []
        var tile_layers = {}

        function load_layers() {
            layers_name = []
            tile_layers = {}
            baseLayers.forEach(layer => {
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

    // ############ SQUADRATS TILES ############
    {
        var style = {
            name: "yard(inho)",
            weight : 2,
            opacity: 0.6,
            fillOpacity : 0.4,
            color : "blue",
        }
        var geojson


        function squadrats_display(data) {
            return L.geoJSON(data, style).addTo(mymap)
        }

        // center on cluster when click on button
        $("#squadrats-center").on("click", function () {
            turf.featureEach(geojson, function (feature) {
                if ((feature.properties.kind=="cluster")
                    && (feature.properties.size>0)) {
                    var bbox = turf.bbox(feature)
                    mymap.fitBounds([[bbox[1], bbox[0]], [bbox[3], bbox[2]]]);
                }
            })
        })

        function load_squadrats_tiles(level, cache="default") {
            fetch("gen/results/kikourou_tiles.geojson", {cache: cache})
            .then(response => response.json())
            .then(data => {
                geojson = data
                squadrats_display(geojson)
            });
        }


        $("#reload").on("click", function() {
            load_squadrats_tiles($("#level").val(), "reload")
        })

        load_squadrats_tiles()
    }

})
