const tileWidth = 64;
const tileHeight = 64;

const tileIdToBiom = {
    "0": 1, // Sea
    "1": 2, // Sentry
    "2": 6, // SDK
    "3": 5, // Processing 
    "4": 4, // Docs
    "5": 3, // Ingest
    "6": 7,
    "7": 8,
    "-1": 1,
    "-2": 2,
    "-3": 3,
    "-4": 4,
    "-5": 5,
    "-6": 6,
    "-7": 7,
    "-8": 8,
    "-9": 9,
    "-10": 10,
    "-11": 11,
    "-12": 12,
    "-13": 13,
    "-14": 14,
}

const tileIdToTileset = {
    "0": "tileset_mixed",
    "1": "tileset_mixed",
    "2": "tileset_mixed",
    "3": "tileset_mixed",
    "4": "tileset_mixed",
    "5": "tileset_mixed",
    "6": "tileset_mixed",
    "7": "tileset_mixed",
    "-1": "tileset_decor",
    "-2": "tileset_decor",
    "-3": "tileset_decor",
    "-4": "tileset_decor",
    "-5": "tileset_decor",
    "-6": "tileset_decor",
    "-7": "tileset_decor",
    "-8": "tileset_decor",
    "-9": "tileset_decor",
    "-10": "tileset_decor",
    "-11": "tileset_decor",
    "-12": "tileset_decor",
    "-13": "tileset_decor",
    "-14": "tileset_decor",
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
            let offsetY = -row/2*tileHeight/2;
            let tileId = oneRow[col];

            drawTile("map", tileIdToTileset[tileId + ""], tileIdToBiom[tileId+""], marginX + offsetX + (col)*tileWidth, offsetY + (row)*tileHeight);
        }
    }
}

function drawTileMapFlatTop(data) {
    marginX = tileWidth/4;
    marginY = -5;

    for (let row = 0; row < data.length; row++) {
        var oneRow = data[row];
        let offsetX = 0.75;
        for (let col = 0; col < oneRow.length; col++) {
            let offsetY=0;
            if(col%2 != 0){
                offsetY = tileWidth*0.45;
            }

            let tileId = oneRow[col];

            drawTile("map", tileIdToTileset[tileId + ""], tileIdToBiom[tileId+""], 
                marginX + col*0.75*tileWidth, 
                marginY + offsetY + row*0.86*tileHeight
            );
        }
    }
}


function drawLabel(mapId, text, x, y){
    var ctx = document.getElementById(mapId).getContext('2d');
    ctx.fillStyle = "white";
    ctx.font = "bold 16px Arial";
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    ctx.fillText(text, x*0.75*tileWidth, y*0.83*tileHeight);
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
        area.insertAdjacentHTML('beforeend', `<h2>${countries[key].name}</h2>`);
        area.insertAdjacentHTML('beforeend', `<h3>Provinces:</h3>`);
        for(let i=0; i<countries[key].provinces.length; i++){
            area.insertAdjacentHTML('beforeend', `${countries[key].provinces[i]}`);
            if(i < countries[key].provinces.length-1) {
                area.insertAdjacentHTML('beforeend', `, `);
            }
        }

        area.insertAdjacentHTML('beforeend', `<h3>Residents (and visitors):</h3>`);
        for(let i=0; i<countries[key].residents.length; i++){
            let resident = countries[key].residents[i]
            area.insertAdjacentHTML('beforeend', `<a href="${resident.url}" target="_blank">${resident.name || resident.login }</a>`);

            if(i < countries[key].residents.length-1) {
                area.insertAdjacentHTML('beforeend', `, `);
            }
        }

        area.insertAdjacentHTML('beforeend', `<p class="dot">*</p>`);
    }
}