import {DIRECTION_LEFT, DIRECTION_RIGHT, DIRECTION_UP, DIRECTION_BOTTOM} from "./directions";
import {oneBlockSize} from "./map-constants";
import {map} from "./map";
import {context} from "../widgets/game-board/game-board.component";

let pacmanFrames = new Image()
pacmanFrames.src = '/animations/animations.gif'

export class Pacman {
  x: number; y: number; height: number; width: number; speed: number; direction: number; currentFrame: number; countFrame: number; nextDirection: number;
  constructor(
    x: number,
    y: number,
    height: number,
    width: number,
    speed: number
  ) {
    this.x = x;
    this.y = y;
    this.height = height;
    this.width = width;
    this.speed = speed;
    this.direction = DIRECTION_RIGHT;
    this.nextDirection = DIRECTION_RIGHT;
    this.currentFrame = 1;
    this.countFrame = 7

    setInterval(() => {
      this.changeAnimation();
    }, 100)
  }

  moveProcess() {
    this.changeDirectionIfPossible()
    this.moveForwards()
    if (this.checkCollisions()) {
      this.moveBackwards()
    }
  }
  eat() {
    for (let i = 0; i < map.length; i++) {
      for (let j = 0; j < map[0].length; j++) {
        if (
          map[i][j] == 2 &&
          this.getMapX() == j &&
          this.getMapY() == i
        ) {
          map[i][j] = 0;
        }
      }
    }
  }
  moveBackwards() {
    switch (this.direction) {
      case DIRECTION_RIGHT: this.x -= this.speed; break;
      case DIRECTION_UP: this.y += this.speed; break;
      case DIRECTION_LEFT: this.x += this.speed; break;
      case DIRECTION_BOTTOM: this.y -= this.speed; break;
    }
  }


  moveForwards() {
    switch (this.direction) {
      case DIRECTION_RIGHT: this.x += this.speed; break;
      case DIRECTION_UP: this.y -= this.speed; break;
      case DIRECTION_LEFT: this.x -= this.speed; break;
      case DIRECTION_BOTTOM: this.y += this.speed; break;
    }
  }
  checkCollisions(): boolean {
    return map[this.getMapY()][this.getMapX()] == 1
      || map[this.getMapYRightSide()][this.getMapX()] == 1
      || map[this.getMapY()][this.getMapXRightSide()] == 1
      || map[this.getMapYRightSide()][this.getMapXRightSide()] == 1;
  }
  checkGhostCollisions() {}
  changeDirectionIfPossible() {
    if (this.direction == this.nextDirection) return;
    let tempDirection = this.direction;
    this.direction = this.nextDirection;
    this.moveForwards();
    if (this.checkCollisions()) {
      this.moveBackwards();
      this.direction = tempDirection;
    } else {
      this.moveBackwards();
    }
  }
  changeAnimation() {
    this.currentFrame = (this.currentFrame + 1) % this.countFrame;
  }
  draw() {
    context.save()
    context.translate(this.x + oneBlockSize / 2, this.y + oneBlockSize / 2);
    context.rotate((this.direction * 90 * Math.PI) / 180);

    context.translate(-this.x - oneBlockSize / 2, -this.y - oneBlockSize / 2);

    context.drawImage(
      pacmanFrames,
      (this.currentFrame) * oneBlockSize,
      0,
      oneBlockSize,
      oneBlockSize,
      this.x,
      this.y,
      this.width,
      this.height,
    )

    context.restore();
  }

  getMapX() {
    return parseInt(String(this.x / oneBlockSize));
  }

  getMapY() {
    return parseInt(String(this.y / oneBlockSize));
  }

  getMapXRightSide() {
    return parseInt(String((this.x + 0.99 * oneBlockSize) / oneBlockSize));
  }

  getMapYRightSide() {
    return parseInt(String((this.y + 0.99 * oneBlockSize) / oneBlockSize));
  }
}
