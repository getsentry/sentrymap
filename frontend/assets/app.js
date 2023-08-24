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


function drawLabel(mapId, text, x, y){
    var ctx = document.getElementById(mapId).getContext('2d');
    ctx.fillStyle = "white";
    ctx.font = "bold 16px Arial";
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    let offsetX = 0;
    if(x%2 != 0){
        offsetX = tileWidth/2;
    }
    let offsetY = -y/2*tileHeight;

    ctx.fillText(text,offsetX + (x)*tileWidth, offsetY + (y)*tileHeight);
}


function drawLables(labels) {
    for (let i = 0; i < labels.length; i++) {
        let label = labels[i];
        drawLabel("map", label.text, label.y, label.x);
    }
}


function printCountryInfo(countries) {
    var area = document.getElementById("countryInfoArea");
    for (let key in countries) {
        area.insertAdjacentHTML('beforeend', `<h1>${countries[key].name}</h1>`);
        area.insertAdjacentHTML('beforeend', `<h2>Provinces</h2>`);
        for(let i=0; i<countries[key].provinces.length; i++){
            area.insertAdjacentHTML('beforeend', `${countries[key].provinces[i]}`);
            if(i < countries[key].provinces.length-1) {
                area.insertAdjacentHTML('beforeend', `, `);
            }
        }

        area.insertAdjacentHTML('beforeend', `<h2>Residents (and visitors)</h2>`);
        for(let i=0; i<countries[key].residents.length; i++){
            let resident = countries[key].residents[i]
            area.insertAdjacentHTML('beforeend', `<a href="${resident.url}">${resident.name}</a>`);

            if(i < countries[key].residents.length-1) {
                area.insertAdjacentHTML('beforeend', `, `);
            }
        }
    }
}