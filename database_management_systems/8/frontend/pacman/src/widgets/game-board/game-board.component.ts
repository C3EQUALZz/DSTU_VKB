import {AfterViewInit, Component, ElementRef, Output, ViewChild} from '@angular/core';
import {gameMap} from "../../helpers/gameMap";
import {Pacman} from '../../helpers/pacman';
import {oneBlockSize, wallOffset, wallSpaceWidth} from "../../helpers/map-constants";
import {DIRECTION_BOTTOM, DIRECTION_LEFT, DIRECTION_RIGHT, DIRECTION_UP} from "../../helpers/directions";
import {Ghost} from "../../helpers/ghost";
import {foodColor, FPS, ghostImages, innerColor, pacmanSpeed, wallColor} from "../../helpers/settings-constant";
import {NgIf} from "@angular/common";


export let context: CanvasRenderingContext2D = {} as CanvasRenderingContext2D;
export let score: number = 0;

export function setScore(newScore: number) {
  score = newScore;
}

export function getScore(): number {
  return score;
}

export let randomTargetsForGhosts = [
  {x: oneBlockSize, y: oneBlockSize},
  {x: oneBlockSize, y: (gameMap.length - 2) * oneBlockSize},
  {x: (gameMap[0].length - 2) * oneBlockSize, y: oneBlockSize},
  {
    x: (gameMap[0].length - 2) * oneBlockSize,
    y: (gameMap.length - 2) * oneBlockSize,
  },
];

@Component({
  selector: 'app-game-board',
  standalone: true,
  imports: [
    NgIf
  ],
  templateUrl: './game-board.component.html',
  styleUrl: './game-board.component.scss'
})
export class GameBoardComponent implements AfterViewInit {
  @ViewChild('myCanvas', {static: false}) canvas: ElementRef = {} as ElementRef;
  boardMap: number[][] = [];
  score: number = getScore();
  pacman: Pacman = new Pacman(oneBlockSize, oneBlockSize, oneBlockSize, oneBlockSize, oneBlockSize / 5, this.boardMap);

  game: boolean = true;

  ghosts: Ghost[] = [];

  mapWidth = gameMap[0].length;
  mapHeight = gameMap.length;

  ngAfterViewInit(): void {
    context = this.canvas.nativeElement.getContext('2d');
    if (this.game) this.startGame();
  }

  startGame() {
    this.setNewMap();
    this.createNewPacman();
    this.createNewGhosts();
    let gameInterval = setInterval(() => {
      if (this.score < 219) {
        this.drawElements();
        this.pacman.draw();
        this.pacman.moveProcess();
        this.pacman.eat();
        this.score = getScore();

        this.ghosts.forEach((ghost) => {
          ghost.moveProcess();
          ghost.draw();
        });
      } else {
        clearInterval(gameInterval);
        this.gameWin();
      }
    }, 1000 / FPS)

    window.addEventListener('keydown', (event) => {
      let k = event.keyCode;

      setTimeout(() => {
        if (k == 37 || k == 65) {
          this.pacman.nextDirection = DIRECTION_LEFT
        } // left
        else if (k == 38 || k == 87) {
          this.pacman.nextDirection = DIRECTION_UP
        } // up
        else if (k == 39 || k == 68) {
          this.pacman.nextDirection = DIRECTION_RIGHT
        } // right
        else if (k == 40 || k == 83) {
          this.pacman.nextDirection = DIRECTION_BOTTOM
        } // bottom
      }, 1)
    })
  }

  createNewGhosts() {
    this.ghosts = [
      new Ghost(18 * oneBlockSize, oneBlockSize, oneBlockSize, oneBlockSize, this.pacman.speed / 2, this.pacman, ghostImages[0]),
      new Ghost(10 * oneBlockSize, 10 * oneBlockSize, oneBlockSize, oneBlockSize, this.pacman.speed / 2, this.pacman, ghostImages[1]),
      new Ghost(15 * oneBlockSize, 15 * oneBlockSize, oneBlockSize, oneBlockSize, this.pacman.speed / 2, this.pacman, ghostImages[2]),
      new Ghost(2 * oneBlockSize, 19 * oneBlockSize, oneBlockSize, oneBlockSize, this.pacman.speed / 2, this.pacman, ghostImages[3]),
    ]
  }

  setNewMap() {
    this.boardMap = JSON.parse(JSON.stringify(gameMap));
  }

  createNewPacman(): void {
    if (this.pacman) this.pacman = {} as Pacman;
    this.pacman = new Pacman(
      oneBlockSize,
      oneBlockSize,
      oneBlockSize,
      oneBlockSize,
      oneBlockSize / pacmanSpeed,
      this.boardMap
    )
  }

  createRect(x: number, y: number, width: number, height: number, color: string) {
    context.fillStyle = color;
    context.fillRect(
      x,
      y,
      width,
      height,
    );
  }

  drawElements() {
    context.clearRect(0, 0, this.mapWidth * oneBlockSize, this.mapHeight * oneBlockSize);
    for (let i = 0; i < this.boardMap.length; i++) {
      for (let j = 0; j < this.boardMap[0].length; j++) {
        if (this.boardMap[i][j] == 1) {
          this.createRect(
            j * oneBlockSize,
            i * oneBlockSize,
            oneBlockSize,
            oneBlockSize,
            wallColor,
          )
          if (j > 0 && this.boardMap[i][j - 1] == 1) {
            this.createRect(
              j * oneBlockSize,
              i * oneBlockSize + wallOffset,
              wallSpaceWidth + wallOffset,
              wallSpaceWidth,
              innerColor
            );
          }

          if (j < this.boardMap[0].length - 1 && this.boardMap[i][j + 1] == 1) {
            this.createRect(
              j * oneBlockSize + wallOffset,
              i * oneBlockSize + wallOffset,
              wallSpaceWidth + wallOffset,
              wallSpaceWidth,
              innerColor
            );
          }

          if (i < this.boardMap.length - 1 && this.boardMap[i + 1][j] == 1) {
            this.createRect(
              j * oneBlockSize + wallOffset,
              i * oneBlockSize + wallOffset,
              wallSpaceWidth,
              wallSpaceWidth + wallOffset,
              innerColor
            );
          }

          if (i > 0 && this.boardMap[i - 1][j] == 1) {
            this.createRect(
              j * oneBlockSize + wallOffset,
              i * oneBlockSize,
              wallSpaceWidth,
              wallSpaceWidth + wallOffset,
              innerColor
            );
          }
        }
        if (this.boardMap[i][j] == 2) {
          this.createRect(
            j * oneBlockSize + oneBlockSize / 2,
            i * oneBlockSize + oneBlockSize / 2,
            oneBlockSize / 6,
            oneBlockSize / 6,
            foodColor
          );
        }
      }
    }
  }

  gameWin(): void {
    context.clearRect(0, 0, this.mapWidth * oneBlockSize, this.mapHeight * oneBlockSize);
    context.fillStyle = 'black';
    context.rect(0, 0, this.mapWidth * oneBlockSize, this.mapHeight * oneBlockSize);
    context.font = "64px BalAstral";
    context.fillStyle = "white";
    context.fillText(
      "YOU WIN",
      this.boardMap[0].length * oneBlockSize / 3.5,
      this.boardMap.length * oneBlockSize / 2,
    );
    let resetIcon = document.getElementById('reset__button')!;
    resetIcon.style.display = 'flex'
    this.pacman = {} as Pacman;
    this.ghosts = [];
    this.boardMap = [];
  }

  restartGame(): void {
    this.game = false;
    context.clearRect(0, 0, this.mapWidth * oneBlockSize, this.mapHeight * oneBlockSize);
    let resetIcon = document.getElementById('reset__button')!;
    resetIcon.style.display = 'none'
    setScore(0);
    this.score = 0;
    this.boardMap = []
    this.game = true;
    this.startGame();
  }

  protected readonly oneBlockSize = oneBlockSize;
}
