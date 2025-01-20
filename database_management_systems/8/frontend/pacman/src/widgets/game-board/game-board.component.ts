import {AfterViewInit, Component, ElementRef, ViewChild} from '@angular/core';
import {map} from "../../helpers/map";
import { Pacman } from '../../helpers/pacman';
import {oneBlockSize, wallOffset, wallSpaceWidth} from "../../helpers/map-constants";
import {DIRECTION_BOTTOM, DIRECTION_LEFT, DIRECTION_RIGHT, DIRECTION_UP} from "../../helpers/directions";

export let context: CanvasRenderingContext2D = {} as CanvasRenderingContext2D;

@Component({
  selector: 'app-game-board',
  standalone: true,
  imports: [],
  templateUrl: './game-board.component.html',
  styleUrl: './game-board.component.scss'
})
export class GameBoardComponent implements AfterViewInit {
  @ViewChild('myCanvas', {static: false}) canvas: ElementRef = {} as ElementRef;

  pacman: Pacman = new Pacman(
    oneBlockSize,
    oneBlockSize,
    oneBlockSize,
    oneBlockSize,
    oneBlockSize / 5
  )

  wallColor: string = '#473cdd'
  innerColor: string = '#0a0502'
  foodColor: string = '#FEB897'

  mapWidth = map[0].length;
  mapHeight = map.length;

  ngAfterViewInit(): void {
    context = this.canvas.nativeElement.getContext('2d');
    setInterval(() => {
      this.drawElements();
      this.pacman.draw();
      this.pacman.moveProcess();
      this.pacman.eat();
    }, 100)

    window.addEventListener('keydown', (event) => {
      let k = event.keyCode;

      setTimeout(() => {
        if (k == 37 || k == 65) { this.pacman.nextDirection = DIRECTION_LEFT } // left
        else if (k == 38 || k == 87) { this.pacman.nextDirection = DIRECTION_UP } // up
        else if (k == 39 || k == 68) { this.pacman.nextDirection = DIRECTION_RIGHT } // right
        else if (k == 40 || k == 83) { this.pacman.nextDirection = DIRECTION_BOTTOM } // bottom
      }, 1)
    })
  }

  startGameLoop() {
    const loop = () => {
      this.drawElements(); // Перерисовка карты
      this.pacman.draw();  // Отрисовка Pacman
      requestAnimationFrame(loop); // Запрос следующего кадра
    };
    loop(); // Запуск цикла
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
    for (let i = 0; i < map.length; i++) {
      for (let j = 0; j < map[0].length; j++) {
        if (map[i][j] == 1) {
          this.createRect(
            j * oneBlockSize,
            i * oneBlockSize,
            oneBlockSize,
            oneBlockSize,
            this.wallColor,
          )
          if (j > 0 && map[i][j - 1] == 1) {
            this.createRect(
              j * oneBlockSize,
              i * oneBlockSize + wallOffset,
              wallSpaceWidth + wallOffset,
              wallSpaceWidth,
              this.innerColor
            );
          }

          if (j < map[0].length - 1 && map[i][j + 1] == 1) {
            this.createRect(
              j * oneBlockSize + wallOffset,
              i * oneBlockSize + wallOffset,
              wallSpaceWidth + wallOffset,
              wallSpaceWidth,
              this.innerColor
            );
          }

          if (i < map.length - 1 && map[i + 1][j] == 1) {
            this.createRect(
              j * oneBlockSize + wallOffset,
              i * oneBlockSize + wallOffset,
              wallSpaceWidth,
              wallSpaceWidth + wallOffset,
              this.innerColor
            );
          }

          if (i > 0 && map[i - 1][j] == 1) {
            this.createRect(
              j * oneBlockSize + wallOffset,
              i * oneBlockSize,
              wallSpaceWidth,
              wallSpaceWidth + wallOffset,
              this.innerColor
            );
          }
        }
        if (map[i][j] == 2) {
          this.createRect(
            j * oneBlockSize + oneBlockSize / 3,
            i * oneBlockSize + oneBlockSize / 3,
            oneBlockSize / 3,
            oneBlockSize / 3,
            this.foodColor
          );
        }
      }
    }
  }

  protected readonly oneBlockSize = oneBlockSize;
}
