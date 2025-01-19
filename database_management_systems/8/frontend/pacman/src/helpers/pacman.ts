import {DIRECTION_LEFT, DIRECTION_RIGHT, DIRECTION_UP, DIRECTION_BOTTOM} from "./directions";
import {oneBlockSize} from "./map-constants";
import {map} from "./map";
import {context} from "../widgets/game-board/game-board.component";

let pacmanFrames = new Image()
pacmanFrames.src = '/animations/animations.gif'

export class Pacman {
  x: number; y: number; height: number; width: number; speed: number; direction: number; currentFrame: number; countFrame: number
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
  eat() {}
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
      || map[this.getMapX()][this.getMapYRightSide()] == 1
      || map[this.getMapXRightSide()][this.getMapYRightSide()] == 1;

  }
  checkGhostCollisions() {}
  changeDirectionIfPossible() {}
  changeAnimation() {
    this.currentFrame = this.currentFrame == this.countFrame ? 1 : this.currentFrame + 1;

  }
  draw() {
    context.save()
    context.translate(this.x + oneBlockSize / 2, this.y + oneBlockSize / 2);
    context.rotate((this.direction * 90 * Math.PI) / 180);

    context.translate(-this.x + oneBlockSize / 2, -this.y + oneBlockSize / 2);

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
    return this.x / oneBlockSize;
  }

  getMapY() {
    return this.y / oneBlockSize;
  }

  getMapXRightSide() {
    return (this.x + 0.9999 * oneBlockSize) / oneBlockSize;
  }

  getMapYRightSide() {
    return (this.y + 0.9999 * oneBlockSize) / oneBlockSize;
  }
}
