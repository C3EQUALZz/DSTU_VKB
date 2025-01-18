import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import {GameBoardComponent} from "../widgets/game-board/game-board.component";


@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, GameBoardComponent, GameBoardComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {}
