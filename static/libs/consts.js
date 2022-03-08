export const consts = {
    //mapbox_token : "pk.eyJ1IjoiYmVub2l0Ym91aWxsYXJkIiwiYSI6ImNreDRpeTIydjF2c28ycG9id2RmMml0ODYifQ.wsvdzJ5MTdM9tGss2HDS4w",
    mapbox_token : "pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw",

    baseLayers :[
       {
            name: "OSM Fr",
            maxZoom: 19,
            attribution: false,
            url: 'https://{s}.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png'
        },
        {
            name: "OSM Cyclo",
            maxZoom: 20,
            attribution: false,
            url: 'https://{s}.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png'
        },
        {
            name: "OSM Topo",
            maxZoom: 17,
            attribution: false,
            url: 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png'
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
            name: "Google Maps",
            url: 'http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
            subdomains:['mt0','mt1','mt2','mt3'],
            attribution: false,
            maxZoom: 20
        },
        {
            name: "IGN Cassini",
            url: 'https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET=PM&FORMAT={format}&LAYER={layer}&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}',
            attribution: false,
            maxZoom: 15,
            apikey: 'an7nvfzojv5wa96dsga5nk8w',
            layer: 'GEOGRAPHICALGRIDSYSTEMS.CASSINI',
            format: 'image/jpeg',
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
    ],

    panes: [
        {name:"grid", zIndex:250},
        {name:"squadrats", zIndex:300},
    ],

}

export const styles = {
    tiles : {
        pane: 'squadrats',

        cluster : {
            name: "yard(inho)",
            weight : 3,
            opacity: 0.5,
            fillOpacity : 0.3,
            color : "#CC6633",
        },
        "sub-cluster": {
            name: "clusters",
            weight : 0,
            opacity: 0.4,
            fillOpacity : 0.15,
            color : "blue",
        },
        max_square: {
            name: "über",
            weight : 3,
            fillOpacity : 0,
            opacity : 0.7,
            color : "green"
        },
        tiles: {
            name: "carrés",
            weight : 2,
            opacity: 0.4,
            fillOpacity : 0.25,
            color : "blue"
        },
        unvisited: {
            name: "non visité",
            weight : 1,
            opacity: 0.8,
            fillOpacity : 0.1,
            color : "red"
        },
    },

    grid : {
        pane: 'grid',
        style : {
          'color': "#bbb",
          'weight': 2,
          'opacity': 0.7,
        }
    }

}