import { oneBlockSize } from "./map-constants";
import { gameMap } from "./gameMap";
import {DIRECTION_BOTTOM, DIRECTION_LEFT, DIRECTION_RIGHT, DIRECTION_UP} from "./directions";

export class Character {
  x: number;
  y: number;
  width: number;
  height: number;
  speed: number;
  targetX: number;
  targetY: number;
  direction: number;
  nextDirection: number;

  constructor(x: number, y: number, width: number, height: number, speed: number) {
    this.x = x;
    this.y = y;
    this.width = width;
    this.height = height;
    this.speed = speed;
    this.direction = DIRECTION_RIGHT; // Направление движения
    this.nextDirection = DIRECTION_RIGHT;
    this.targetX = 0;
    this.targetY = 0;

  }

  moveProcess() {
    this.changeDirectionIfPossible()
    this.moveForwards()
    if (this.checkCollisions()) {
      this.moveBackwards()
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
    return gameMap[this.getMapY()][this.getMapX()] == 1
      || gameMap[this.getMapYRightSide()][this.getMapX()] == 1
      || gameMap[this.getMapY()][this.getMapXRightSide()] == 1
      || gameMap[this.getMapYRightSide()][this.getMapXRightSide()] == 1;
  }

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
