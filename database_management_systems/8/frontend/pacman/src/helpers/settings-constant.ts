export const FPS = 45;
export const pacmanSpeed = 5; // oneBlockSize divide pacmanSpeed
export const ghostRadius = 10;

// ghost images
const $red_ghost = new Image()
$red_ghost.src = 'ghosts/red_ghost.png';

const $orange_ghost = new Image()
$orange_ghost.src = 'ghosts/orange_ghost.png';

const $pink_ghost = new Image()
$pink_ghost.src = 'ghosts/pink_ghost.png';

const $cyan_ghost = new Image()
$cyan_ghost.src = '/ghosts/cyan_ghost.png';
export const ghostImages: HTMLImageElement[] = [
  $red_ghost,
  $orange_ghost,
  $pink_ghost,
  $cyan_ghost,
]

// map colors
export const wallColor: string = '#473cdd'
export const innerColor: string = '#0a0502'
export const foodColor: string = '#fab699'
