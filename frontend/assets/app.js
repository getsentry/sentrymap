const tileWidth = 64;
const tileHeight = 96;

const tileIdToBiom = {
    0: 1,
    1: 2,
    2: 3,
    3: 4,
    4: 5,
    5: 6,
    6: 7,
    7: 8,
}

const tileIdToTileset = {
    0: "tileset_mixed",
    1: "tileset_mixed",
    2: "tileset_mixed",
    3: "tileset_mixed",
    4: "tileset_mixed",
    5: "tileset_mixed",
    6: "tileset_mixed",
    7: "tileset_mixed",
}


function putImage(mapId, stuffId, x, y){
    var ctx = document.getElementById(mapId).getContext('2d');
    ctx.drawImage(window.stuff[stuffId], x, y);            
}


function drawTile(mapId, tileSet, tileId, x, y){
    var ctx = document.getElementById(mapId).getContext('2d');
    ctx.drawImage(window.stuff[tileSet], (tileId-1)*tileWidth, 0, tileWidth, tileHeight, x, y, tileWidth, tileHeight);
}


function drawTileMap(data) {
    marginX = tileWidth/4;

    for (let row = 0; row < data.length; row++) {
        var oneRow = data[row];
        let offsetX = 0;
        if(row%2 != 0){
            offsetX = tileWidth/2;
        }
        for (let col = 0; col < oneRow.length; col++) {
            let offsetY = -row/2*tileHeight;
            let tileId = oneRow[col];
            drawTile("map", tileIdToTileset[tileId], tileIdToBiom[tileId], marginX + offsetX + (col)*tileWidth, offsetY + (row)*tileHeight);
        }
    }
}