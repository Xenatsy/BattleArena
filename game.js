const canvas = document.getElementsByTagName("canvas")[0];
const ctx = canvas.getContext("2d");


canvas.style.cursor = "pointer";
canvas.style.touchAction = "none";
function handleClick(x, y) {
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    x = (x - rect.left) * scaleX;
    y = (y - rect.left) * scaleY;

    mouseDown(x, y);
}

canvas.addEventListener("click", (e) => {
    e.preventDefault();
    handleClick(e.clientX, e.clientY);
})

canvas.addEventListener("touchstart", (e) => {
    e.preventDefault();
    if (e.touches.length === 1) {
        handleClick(e.touches[0].clientX, e.touches[0].clientY);
    }
}, { passive: false });

canvas.addEventListener('touchmove', (e) => {
    e.preventDefault();
}, { passive: false });

let isOver = false;
let size = 0;

let board = [];
let offsetX = 5 * size / 2 + canvas.width / 2;
let offsetY = 5 * size / 2 + canvas.height / 2;
let mouseState = "empty";
let from = { x: -1, y: -1 };
let to = { x: -1, y: -1 };

let start = { x: -1, y: -1 };
let end = { x: -1, y: -1 };

let mouse = { x: -1, y: -1 };

function mouseMove(event) {
    const rect = canvas.getBoundingClientRect();
    const mouseX = event.clientX - rect.left;
    const mouseY = event.clientY - rect.top;

    board.forEach(element => {
        if (element.isPointIn(mouseX - offsetX, mouseY - offsetY)) {
            element.borderColor = "red";
            mouse.x = element.x * size + element.size / 2 + offsetX;
            mouse.y = element.y * size + element.size / 2 + offsetY;
        } else {
            element.borderColor = "black";
        }
    });
    draw();
}

function isWin() {
    for (const element of board) {
        if (element.figure) {
            console.log(element.figure.team);
            if (element.figure.team == "blue") {
                return false;
            }
        }

    }
    return true;
}


function mouseDown(x = null, y = null, event = null) {
    let mouseX;
    let mouseY;
    if (event) {
        const rect = canvas.getBoundingClientRect();
        mouseX = event.clientX - rect.left;
        mouseY = event.clientY - rect.top;
    }
    else {
        mouseX = x;
        mouseY = y;
    }


    board.forEach(element => {
        if (element.isPointIn(mouseX - offsetX, mouseY - offsetY)) {
            switch (mouseState) {
                case "empty": {
                    start = { x: -1, y: -1 };
                    end = { x: -1, y: -1 };
                    if (element.figure && element.figure.team == "yellow") {
                        mouseState = "chosen";

                        element.isSelected = true;
                        from.x = element.x;
                        start.x = element.x * size + size / 2 + offsetX;
                        from.y = element.y;
                        start.y = element.y * size + size / 2 + offsetY;
                    }
                    break;
                }
                case "chosen": {
                    element.isSelected = false;
                    to.x = element.x;
                    end.x = element.x * size + size / 2 + offsetX;
                    to.y = element.y;
                    end.y = element.y * size + size / 2 + offsetY;

                    let equalCondition = from.x == to.x && from.y == to.y;

                    if (!equalCondition) {
                        if (distance(from.x, from.y, to.x, to.y) == 1) {
                            // Правильный расчет индексов
                            let fromIndex = from.x * 5 + from.y;
                            let toIndex = to.x * 5 + to.y;

                            let fromF = board[fromIndex].figure;
                            let toF = board[toIndex].figure;
                            if (toF) {
                                if (toF.team == "blue") { // Атакуем фигуру врага
                                    toF.health -= fromF.damage;
                                    if (toF.health <= 0) {
                                        board[toIndex].figure = fromF;
                                        board[fromIndex].figure = null;
                                        mouseState = "empty";
                                    }

                                    AITurn();

                                }
                            } else if (fromF && !toF) {
                                // Ход Игрока
                                board[toIndex].figure = fromF;
                                board[fromIndex].figure = null;
                                mouseState = "empty";

                                // Ход ИИ
                                AITurn();
                            }
                        }
                    }
                    else {
                        mouseState = "empty";
                        start = { x: -1, y: -1 };
                        end = { x: -1, y: -1 };
                    }
                    break;
                }
            }
        }
    });
    draw();
}

class Point {
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }
}

function AITurn() {
    let possibleMoves = [];
    let possibleAttax = [];

    board.forEach((element, index) => {
        if (element.figure && element.figure.team == "blue") {
            let x = Math.floor(index / 5); // Получаем x из индекса
            let y = index % 5; // Получаем y из индекса

            // Проверяем всех соседей (комментированные соседи расположены выше)
            const neighbors = [
                // { x: x - 1, y: y - 1 }, 
                { x: x - 1, y: y },
                { x: x - 1, y: y + 1 },
                //  { x: x, y: y - 1 }, 
                { x: x, y: y + 1 },
                // { x: x + 1, y: y - 1 }, 
                { x: x + 1, y: y },
                { x: x + 1, y: y + 1 }
            ];

            neighbors.forEach(neighbor => {
                if (neighbor.x >= 0 && neighbor.x < 5 && neighbor.y >= 0 && neighbor.y < 5) {
                    let neighborIndex = neighbor.x * 5 + neighbor.y;
                    if (board[neighborIndex].figure) {
                        if (board[neighborIndex].figure.team == "yellow") {
                            possibleAttax.push({
                                from: index,
                                to: neighborIndex,
                            });
                        }
                    }
                    else {
                        possibleMoves.push({
                            from: index,
                            to: neighborIndex,
                        });

                    }
                }
            });
        }
    });
    if (possibleAttax.length > 0) {
        let chosenAttack = possibleAttax[Math.floor(Math.random() * possibleAttax.length)];
        let toF = board[chosenAttack.to].figure;
        let fromF = board[chosenAttack.from].figure;
        toF.health -= fromF.damage;
        if (toF.health <= 0) {
            board[chosenAttack.to].figure = board[chosenAttack.from].figure;
            board[chosenAttack.from].figure = null;
        }
    }
    else if (possibleMoves.length > 0) {
        let possibleMove = possibleMoves[Math.floor(Math.random() * possibleMoves.length)];
        let fromF = board[possibleMove.from].figure;
        board[possibleMove.to].figure = fromF;
        board[possibleMove.from].figure = null;
    }
    draw();
}

function onResize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    size = Math.min(canvas.width / 5, canvas.height / 5);
    offsetX = -5 * size / 2 + canvas.width / 2;
    offsetY = -5 * size / 2 + canvas.height / 2;

    start.x = from.x * size + size / 2 + offsetX;
    start.y = from.y * size + size / 2 + offsetY;
    end.x = to.x * size + size / 2 + offsetX;
    end.y = to.y * size + size / 2 + offsetY;

    board.forEach((cell) => {
        cell.size = size;
    });
    draw();
}
window.onmousemove = mouseMove;
window.onmousedown = mouseDown;

window.onresize = onResize;
window.onload = init;
window.onfocus = onResize;

class Figure {
    constructor(health, damage, team) {
        this.health = health;
        this.damage = damage;
        this.team = team;
    }
}

class Cell {
    constructor(x, y, size, color, borderColor, borderPadding, figure = null) {
        this.x = x;
        this.y = y;
        this.size = size;
        this.backgroundColor = color;
        this.borderPadding = borderPadding;
        this.borderColor = borderColor;

        this.figure = figure;

        this.isSelected = false;

    }
    draw(offsetX, offsetY) {
        const size = this.size;
        ctx.strokeStyle = this.borderColor;

        ctx.strokeRect(this.x * size + offsetX, this.y * size + offsetY, size - 5, size - 5);
        ctx.fillStyle = this.backgroundColor;
        ctx.fillRect(this.x * size + offsetX, this.y * size + offsetY, size - 5, size - 5);

        if (this.figure) {
            ctx.strokeStyle = this.isSelected ? "red" : this.figure.team;
            ctx.fillStyle = this.figure.team;

            ctx.beginPath();
            ctx.arc(
                (2 * this.x * size + 2 * offsetX + size - 5) / 2,
                (2 * this.y * size + 2 * offsetY + size - 5) / 2,
                (size - 5) / 2 - 5,
                0, 2 * Math.PI
            );

            ctx.fill();
            ctx.stroke();
            ctx.fillStyle = "black";
            ctx.font = `${size / 5}px consolas`;
            ctx.fillText(
                `❤️${this.figure.health}`,
                this.x * size + offsetX,
                this.y * size + offsetY + size / 2,
            )
            ctx.fillText(
                `🗡️${this.figure.damage}`,
                this.x * size + offsetX + size / 2,
                this.y * size + offsetY + size / 2,
            )

        }
    }
    isPointIn(x0, y0) {
        const x = this.x;
        const y = this.y;
        const size = this.size;
        return (x * size < x0) && (x0 < x * size + size) &&
            (y * size < y0) && (y0 < y * size + size);
    }
}

function distance(x1, y1, x2, y2) {
    return Math.max(Math.abs(x1 - x2), Math.abs(y1 - y2));
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    board.forEach(element => {
        element.draw(offsetX, offsetY);
    });

    if (isWin()) {
        ctx.fillStyle = "white";
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "black";
        const text = "You won!";
        const metrics = ctx.measureText(text);
        const actualX = canvas.width / 2 - metrics.width / 2;
        ctx.fillText(text, actualX, canvas.height / 2);
    }
}
function init() {
    onResize();
    for (i = 0; i < 5; i++) {
        for (j = 0; j < 5; j++) {
            board.push(new Cell(i, j, size, "white", "black", 10));
        }
    }
    for (x = 0; x < 5; x++) {
        let value = 5 - Math.abs(x - 2);
        let f1 = new Figure(value, value, "blue");
        let f2 = new Figure(value, value, "yellow");
        i1 = 0;
        i2 = 4;
        j = x;
        board[i1 + j * 5].figure = f1;
        board[i2 + j * 5].figure = f2;

    }
    draw();
}

