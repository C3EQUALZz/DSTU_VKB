import {AfterViewInit, Component, ElementRef, ViewChild} from '@angular/core';

let map: number[][] = [
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
  [1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1],
  [1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1],
  [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
  [1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1],
  [1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1],
  [1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1],
  [0, 0, 0, 0, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0],
  [1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1],
  [2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2],
  [1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 2, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1],
  [0, 0, 0, 0, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 0, 0, 0, 0],
  [0, 0, 0, 0, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0],
  [1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1],
  [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
  [1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1],
  [1, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 1],
  [1, 1, 2, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 2, 1, 1],
  [1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1],
  [1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1],
  [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
];

@Component({
  selector: 'app-game-board',
  standalone: true,
  imports: [],
  templateUrl: './game-board.component.html',
  styleUrl: './game-board.component.scss'
})
export class GameBoardComponent implements AfterViewInit {
  @ViewChild('myCanvas', {static: false}) canvas: ElementRef = {} as ElementRef;

  context: CanvasRenderingContext2D = {} as CanvasRenderingContext2D;

  oneBlockSize = 35;
  wallSpaceWidth = this.oneBlockSize / 1.6;
  wallOffset = (this.oneBlockSize - this.wallSpaceWidth) / 2;
  wallColor: string = '#473cdd'
  innerColor: string = '#0a0502'
  mapWidth = map[0].length; // Количество колонок (21)
  mapHeight = map.length; // Количество строк (23)

  ngAfterViewInit(): void {
    this.context = this.canvas.nativeElement.getContext('2d');
    this.drawWalls();
  }

  createRect(x: number, y: number, width: number, height: number, color: string) {
    this.context.fillStyle = color;
    this.context.fillRect(
      x,
      y,
      width,
      height,
    );
  }

  drawWalls() {
    for (let i = 0; i < map.length; i++) {
      for (let j = 0; j < map[0].length; j++) {
        if (map[i][j] == 1) {
          this.createRect(
            j * this.oneBlockSize,
            i * this.oneBlockSize,
            this.oneBlockSize,
            this.oneBlockSize,
            this.wallColor,
          )
          if (j > 0 && map[i][j - 1] == 1) {
            this.createRect(
              j * this.oneBlockSize,
              i * this.oneBlockSize + this.wallOffset,
              this.wallSpaceWidth + this.wallOffset,
              this.wallSpaceWidth,
              this.innerColor
            );
          }

          if (j < map[0].length - 1 && map[i][j + 1] == 1) {
            this.createRect(
              j * this.oneBlockSize + this.wallOffset,
              i * this.oneBlockSize + this.wallOffset,
              this.wallSpaceWidth + this.wallOffset,
              this.wallSpaceWidth,
              this.innerColor
            );
          }

          if (i < map.length - 1 && map[i + 1][j] == 1) {
            this.createRect(
              j * this.oneBlockSize + this.wallOffset,
              i * this.oneBlockSize + this.wallOffset,
              this.wallSpaceWidth,
              this.wallSpaceWidth + this.wallOffset,
              this.innerColor
            );
          }

          if (i > 0 && map[i - 1][j] == 1) {
            this.createRect(
              j * this.oneBlockSize + this.wallOffset,
              i * this.oneBlockSize,
              this.wallSpaceWidth,
              this.wallSpaceWidth + this.wallOffset,
              this.innerColor
            );
          }
        }
      }
    }
  }
}
