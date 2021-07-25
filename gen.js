#!/usr/bin/env node

function gen(_n) {
    const n = (~~_n) || 4;
    // console.log({_n});
    let data = [];
    for (let i = 0; i < n; i++) {
        data.push(Array(n).fill(0))
    }

    let coords = [];
    for (let i = 0; i< n; i++) {
        for (let j = 0; j < n; j++) {
            coords.push([i, j]);
        }
    }
    let shuffledCoords = shuffle(coords);
    // let shuffledCoords = coords;

    for (let coord of shuffledCoords) {
        let emptyNbors = getNeighbors(n, coord).filter(it => dataAt(data, it) === 0);
        if (emptyNbors.length <= 1) {
            continue;
        }

        if (isArticulationPoint(data, coord)) {
            // console.log(' is articulation point', coord);
            continue;
        }

        data = dataSet(data, coord, 1);
    }

    return data;
}

function isArticulationPoint(data, coord) {
    const n = data.length;

    const emptyNbors = getNeighbors(n, coord).filter(it => dataAt(data, it) === 0);

    const touched = {};
    touched[JSON.stringify(coord)] = true;
    const stack = [];
    stack.push(emptyNbors[0]);
    while (stack.length > 0) {
        const curr = stack.pop();
        if (touched[JSON.stringify(curr)]) {
            continue;
        }
        touched[JSON.stringify(curr)] = true;
        const nbors = getNeighbors(n, curr).filter(it => dataAt(data, it) === 0);
        for (let nbor of nbors) {
            if (touched[JSON.stringify(nbor)]) {
                continue;
            } else {
                stack.push(nbor);
            }
        }
    }

    const otherNeighbors = emptyNbors.slice(1);
    for (let nbor of otherNeighbors) {
        if (!(touched[JSON.stringify(nbor)])) {
            // console.log({touched});
            // process.exit(0);
            return true;
        }
    }
    return false;
}

function dataAt(data, coord) {
    return data[coord[0]][coord[1]];
}

function dataSet(data, coord, value) {
    const newData = data.map(row => [...row]);
    newData[coord[0]][coord[1]] = value;
    return newData;
}

function shuffle(arr) {
    return arr
        .map((it) => [ it, Math.random() ])
        .sort((a,b) => a[1] - b[1])
        .map(([it, s]) => it);
}

function getNeighbors(n, coords) {
    const [r, c] = coords;
    const candidates = [[r+1, c+2], [r+1, c-2], [r-1, c+2], [r-1, c-2], [r+2, c+1], [r+2, c-1], [r-2, c+1], [r-2, c-1]];
    return candidates.filter(it => it[0] >= 0 && it[0] < n && it[1] >= 0 && it[1] < n);
}

// console.log(JSON.stringify(gen(process.argv[2])));
const filled = gen(process.argv[2]);
for (let row of filled) {
    console.log(row.map(it => it === 0 ? '⬜' : '⬛').join(''));
}
