# dijkstras-algorithm

Graphical representation of [Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra's_algorithm) for path finding.

**Graphical**
Whole idea behind it is grid of boxes (created class) with specific attributes

## Basic controls
  
  ### movement
  to select each box you can use mouse (just by hovering) <br>
  or by arrows (neovim-like movement is also supported)
  
  **Mouse control** 
    <ul>
      <li>**left mouse** places wall</li>
      <li>**right mouse** places target</li>
    </ul>
  **Keyboard controls**
    <ul>
      <li>**spacebar** starts algorithm</li>
      <li>**z** places wall</li>
      <li>**x** places target</li>
    </ul>
## Type of boxes
 <h3>Start</h3>
 <p>Starting box (name should be self explaining)</p>
 <h3>Target</h3>
 <p>Box you want to get</p>
 <h3>Wall</h3>
 <p>Box that cannot be use to get to the target</p>
 

## Requirements
<ul>
  <li>Pygame</li>
  <li>Tkinter</li>
</ul>
Note: you will need also their requirements


## Roadmap
<ul>
  <li>Diagonal movement</li>
  <li>Remapable controls</li>
  <li>Better GUI</li>
  <li>Terminal version</li>
</ul>

### Disclaimer
  this repository implements some part of this [video tutorial](https://www.youtube.com/watch?v=QNpUN8gBeLY)
