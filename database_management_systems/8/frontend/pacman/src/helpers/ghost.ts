import { Character } from "./character";
import {DIRECTION_BOTTOM, DIRECTION_LEFT, DIRECTION_RIGHT, DIRECTION_UP} from "./directions";
import {oneBlockSize} from "./map-constants";
import {context, randomTargetsForGhosts} from "../widgets/game-board/game-board.component";
import {Pacman} from "./pacman";
import {gameMap} from "./gameMap";
import {ghostRadius} from "./settings-constant";

type MapType = number[][];

interface Position {
  x: number;
  y: number;
  rightX: number;
  rightY: number;
  moves: number[];
}

export class Ghost extends Character {
  randomTargetIndex: number; target: { x: number; y: number }; range: number; pacman: Pacman; image: HTMLImageElement;
  constructor(x: number, y: number, width: number, height: number, speed: number, pacman: Pacman, image: HTMLImageElement) {
    super(x, y, width, height, speed);
    this.pacman = pacman
    this.range = ghostRadius;
    this.image = image;
    this.randomTargetIndex = parseInt(String(Math.random() * 4));
    this.target = randomTargetsForGhosts[this.randomTargetIndex];
    setInterval(() => {
      this.changeRandomDirection();
    }, 3000);
  }

  isInRange() {
    let xDistance = Math.abs(this.pacman.getMapX() - this.getMapX());
    let yDistance = Math.abs(this.pacman.getMapY() - this.getMapY());
    return Math.sqrt(xDistance * xDistance + yDistance * yDistance) <=
      this.range;

  }

  changeRandomDirection() {
    let addition = 1;
    this.randomTargetIndex += addition;
    this.randomTargetIndex = this.randomTargetIndex % 4;
  }

  draw(): void {
    context.drawImage(
      this.image,
      this.x,
      this.y,
      oneBlockSize * 1.2,
      oneBlockSize * 1.2,
    );
  }

  override moveProcess() {
    if (this.isInRange()) {
      this.target = {
        x: this.pacman.x,
        y: this.pacman.y,
      };
    } else {
      this.target = randomTargetsForGhosts[this.randomTargetIndex];
    }
    this.changeDirectionIfPossible();
    this.moveForwards();
    if (this.checkCollisions()) {
      this.moveBackwards();
      return;
    }
  }


  override changeDirectionIfPossible() {
    let tempDirection = this.direction;
    this.direction = this.calculateNewDirection(
      gameMap,
      parseInt(String(this.target.x / oneBlockSize)),
      parseInt(String(this.target.y / oneBlockSize))
    );
    if (
      this.getMapY() != this.getMapYRightSide() &&
      (this.direction == DIRECTION_LEFT ||
        this.direction == DIRECTION_RIGHT)
    ) {
      this.direction = DIRECTION_UP;
    }
    if (
      this.getMapX() != this.getMapXRightSide() &&
      this.direction == DIRECTION_UP
    ) {
      this.direction = DIRECTION_LEFT;
    }
    this.moveForwards();
    if (this.checkCollisions()) {
      this.moveBackwards();
      this.direction = tempDirection;
    } else {
      this.moveBackwards();
    }
  }

  calculateNewDirection(map: MapType, destX: number, destY: number) {
    let mp = [];
    for (let i = 0; i < map.length; i++) {
      mp[i] = map[i].slice();
    }

    let queue: Position[] = [
      {
        x: this.getMapX(),
        y: this.getMapY(),
        rightX: this.getMapXRightSide(),
        rightY: this.getMapYRightSide(),
        moves: [],
      },
    ];
    while (queue.length > 0) {
      let poped: Position = queue.shift()!;
      if (poped.x == destX && poped.y == destY) {
        return poped.moves[0];
      } else {
        mp[poped.y][poped.x] = 1;
        let neighborList = this.addNeighbors(poped, mp);
        for (let i = 0; i < neighborList.length; i++) {
          queue.push(neighborList[i]);
        }
      }
    }

    return DIRECTION_RIGHT;
  }
  /**
   * Добавляет соседние клетки в очередь на основе текущей позиции.
   * @param popped Текущая позиция.
   * @param mp Карта с пометками.
   * @returns Массив соседних позиций.
   */
  addNeighbors(
    popped: Position,
    mp: MapType
  ): Position[] {
    const queue: Position[] = [];
    const numOfRows = mp.length;
    const numOfColumns = mp[0].length;

    if (
      popped.x - 1 >= 0 &&
      mp[popped.y][popped.x - 1] !== 1
    ) {
      const tempMoves = [...popped.moves, DIRECTION_LEFT];
      queue.push({ x: popped.x - 1, y: popped.y, rightX: popped.rightX - 1, rightY: popped.rightY, moves: tempMoves });
    }
    if (
      popped.x + 1 < numOfColumns &&
      mp[popped.y][popped.x + 1] !== 1
    ) {
      const tempMoves = [...popped.moves, DIRECTION_RIGHT];
      queue.push({ x: popped.x + 1, y: popped.y, rightX: popped.rightX + 1, rightY: popped.rightY, moves: tempMoves });
    }
    if (
      popped.y - 1 >= 0 &&
      mp[popped.y - 1][popped.x] !== 1
    ) {
      const tempMoves = [...popped.moves, DIRECTION_UP];
      queue.push({ x: popped.x, y: popped.y - 1, rightX: popped.rightX, rightY: popped.rightY - 1, moves: tempMoves });
    }
    if (
      popped.y + 1 < numOfRows &&
      mp[popped.y + 1][popped.x] !== 1
    ) {
      const tempMoves = [...popped.moves, DIRECTION_BOTTOM];
      queue.push({ x: popped.x, y: popped.y + 1, rightX: popped.rightX, rightY: popped.rightY + 1, moves: tempMoves });
    }
    return queue;
  }
}
