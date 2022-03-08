function TileFromCoord(lat, lon, level=17) {
    let n = Math.pow(2, level);
    let x = Math.floor(n * (lon + 180 ) / 360);
    let lat_r = lat*Math.PI/180;
    let y = Math.floor(n * ( 1 - ( Math.log( Math.tan(lat_r) + 1/Math.cos(lat_r) ) / Math.PI ) ) / 2);
    return [x, y];
}
function LatLngFromTile(x, y, level=17) {
    let n = Math.pow(2, level);
    let lat = Math.atan( Math.sinh( Math.PI * (1 - 2*y / n ) ) ) * 180.0 / Math.PI;
    let lon = x / n * 360.0 - 180.0;
    return L.latLng(lat, lon);
}
function coordsFromTile(x, y, level=17) {
    let n = Math.pow(2, level);
    let lat = Math.atan( Math.sinh( Math.PI * (1 - 2*y / n ) ) ) * 180.0 / Math.PI;
    let lon = x / n * 360.0 - 180.0;
    return [lat, lon];
}

function boundsFromTile(x, y, level=17) {
    return L.latLngBounds(LatLngFromTile(x, y, level), LatLngFromTile(x+1, y+1, level));
}
function boundsFromTileId(tileId, level=17) {
    let part = tileId.split('_')
    let x = parseInt(part[0])
    let y = parseInt(part[1])
    return boundsFromTile(x, y, level)
}

function geojsonFromTile(x, y, level=17) {
    let p1 = coordsFromTile(x, y, level)
    let p2 = coordsFromTile(x+1, y+1, level)

    return turf.polygon([[
        [p1[1], p1[0]],
        [p1[1], p2[0]],
        [p2[1], p2[0]],
        [p2[1], p1[0]],
        [p1[1], p1[0]],
    ]])
}
let COORDINATES_PRECISION= 7

function lon2squadrat(lon, z) {
    return (Math.floor((lon + 180) / 360 * Math.pow(2, z)));
}
function lat2squadrat(lat, z) {
    return (Math.floor((1 - Math.log(Math.tan(lat * Math.PI / 180) + 1 / Math.cos(lat * Math.PI / 180)) / Math.PI) / 2 * Math.pow(2, z)));
}
function squadrat2lon(x, z) {
    return +(x / Math.pow(2, z) * 360 - 180).toFixed(COORDINATES_PRECISION);
}
function squadrat2lat(y, z) {
    const n = Math.PI - 2 * Math.PI * y / Math.pow(2, z);
    return +(180 / Math.PI * Math.atan(0.5 * (Math.exp(n) - Math.exp(-n)))).toFixed(COORDINATES_PRECISION);
}

function LeafletLatLngToGeojson(latlng) {
    return [latlng.lng, latlng.lat]
}

function lines2geojson(lines, zoom) {
    return {
        type: 'FeatureCollection',
        features: lines.map(function (d) {
            return {
                type: 'Feature',
                geometry: {
                    type: 'Polygon',
                    coordinates: [
                        d.map(function (e) {
                            return [
                                +squadrat2lon(e.x, zoom),
                                +squadrat2lat(e.y, zoom),
                            ];
                        }),
                    ],
                },
            };
        }),
    };
}

function generateGridSegments(mymap, zoom, limit=false) {
    const maxSquadratNr = Math.pow(2, zoom);
    const minSquadratNr = 0;

    const segments = [];
    const bounds = mymap.getBounds();
    let nw;
    let se;

    nw = bounds.getNorthWest();
    se = bounds.getSouthEast();

    nw.x = lon2squadrat(nw.lng, zoom);
    nw.y = lat2squadrat(nw.lat, zoom);
    se.x = lon2squadrat(se.lng, zoom)+1;
    se.y = lat2squadrat(se.lat, zoom)+1;
        const width = Math.abs(nw.x - se.x);
    const height = Math.abs(nw.y - se.y);
    if (limit && (width * height > limit)) {
        return false
    }

    for (let x = nw.x; x < se.x; x++) {
        segments.push([{
            x: +x,
            y: +nw.y,
        }, {
            x: +x,
            y: +se.y,
        }]);
    }

    for (let y = nw.y; y < se.y; y++) {
        segments.push([{
            x: +nw.x,
            y: +y,
        }, {
            x: +se.x,
            y: +y,
        }]);
    }

    return segments;
}

class TilesStorage {
    constructor(t={}) {
       this.tiles = t
       this.count = 0
    }
    has(x, y) {
        if (this.tiles.hasOwnProperty(x)) {
            return this.tiles[x].includes(y)
        } else {
            return false
        }
    }

    add(x, y) {
        if (!this.tiles.hasOwnProperty(x)) {
            this.tiles[x] = []
        }
        if (this.tiles[x].includes(y)) {
            return false
        }
        this.tiles[x].push(y)
        this.count++
        return true
    }

    remove(x, y) {
        const index = this.tiles[x].indexOf(5);
        if (index > -1) {
            this.tiles[x].splice(index, 1);
        }
    }

    clear() {
        this.tiles = {}
        this.count = 0
    }

    forEach(callback) {
        $.each(this.tiles, function(x, arr){
            if (Array.isArray(arr)) { // for compatibility to avoid errors
                arr.forEach(function(y) {
                    callback(x*1, y)
                })
            }
        })
    }

    list() {
        var l = []
        this.forEach((x, y) => {
            l.push([x, y])
        })
        return l
    }
}

function on_init(callback, delay=1) {
    setTimeout(callback, delay)
}


// Warn if overriding existing method
if(Array.prototype.equals)
    console.warn("Overriding existing Array.prototype.equals. Possible causes: New API defines the method, there's a framework conflict or you've got double inclusions in your code.");
// attach the .equals method to Array's prototype to call it on any array
Array.prototype.equals = function (array) {
    // if the other array is a falsy value, return
    if (!array)
        return false;

    // compare lengths - can save a lot of time
    if (this.length != array.length)
        return false;

    for (var i = 0, l=this.length; i < l; i++) {
        // Check if we have nested arrays
        if (this[i] instanceof Array && array[i] instanceof Array) {
            // recurse into the nested arrays
            if (!this[i].equals(array[i]))
                return false;
        }
        else if (this[i] != array[i]) {
            // Warning - two different object instances will never be equal: {x:20} != {x:20}
            return false;
        }
    }
    return true;
}
// Hide method from for-in loops
Object.defineProperty(Array.prototype, "equals", {enumerable: false});

function clone(something) {
    return JSON.parse(JSON.stringify(something))
}