import {gameMap} from "./gameMap";
import {context, getScore, setScore} from "../widgets/game-board/game-board.component";
import {Character} from "./character";
import {oneBlockSize} from "./map-constants";

let radius = oneBlockSize / 2;
let isMouthOpening = true;
let angle = 0; // Начальный угол для "рта"

export class Pacman extends Character {

  constructor(x: number, y: number, width: number, height: number, speed: number) {
    super(x, y, width, height, speed);

    setInterval(() => {
      this.updatePacman();
    }, 30)
  }

  eat() {
    for (let i = 0; i < gameMap.length; i++) {
      for (let j = 0; j < gameMap[0].length; j++) {
        if (
          gameMap[i][j] == 2 &&
          this.getMapX() == j &&
          this.getMapY() == i
        ) {
          gameMap[i][j] = 0;
          let newScore = getScore() + 1;
          setScore(newScore);
        }
      }
    }
  }

  draw() {
    context.save();
    context.translate(
      this.x + oneBlockSize / 2,
      this.y + oneBlockSize / 2
    );
    context.rotate((this.direction * 90 * Math.PI) / 180);
    context.translate(
      -this.x - oneBlockSize / 2,
      -this.y - oneBlockSize / 2
    );

    // Рассчитываем начальный и конечный углы дуги для "рта"
    const startAngle = angle * Math.PI; // Начало рта
    const endAngle = (2 - angle) * Math.PI; // Конец рта

    // Рисуем тело Пакмана
    context.fillStyle = "#fdff00";
    context.beginPath();
    context.moveTo(this.x + radius, this.y + radius); // Начальная точка в центре круга
    context.arc(this.x + radius, this.y + radius, radius, startAngle, endAngle); // Рисуем дугу
    context.closePath();
    context.fill();
    context.restore();
  }

  updatePacman() {
    // Анимация рта: открывание и закрывание
    if (isMouthOpening) {
      angle += 0.02;
      if (angle >= 0.3) isMouthOpening = false;
    } else {
      angle -= 0.02;
      if (angle <= 0) isMouthOpening = true;
    }
  }
}
