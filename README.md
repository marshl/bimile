Creates a animated GIF file of a simulated
[Biham–Middleton–Levine traffic model](https://en.wikipedia.org/wiki/Biham%E2%80%93Middleton%E2%80%93Levine_traffic_model)

## Function

The Biham–Middleton–Levine traffic model is a form of cellular automata
in which a number of red and blue squares (cars) are places randomly on a grid.
Red cars will always try and move right, but can only do so if that cell
is unoccupied. Blue cars will always try to move down, but like the red
cars, cannot do so if the way is blocked. This can create some very interesting animations.


## Usage
```
bimile.py [-h] [--frame-skip FRAME_SKIP] [--cell-size CELL_SIZE]
                 scale density frame_count
```

#### Positional arguments:
```scale```
The number of cells high and wide the grid will be.
Try to keep this less than a few hundred.

```density```
The density of the traffic, with 0.0 meaning no cells will be occupied,
and 1.0 meaning all cells will be occupied.
It is best to keep the density between 0.3 and 0.6, with <0.3 usually
causing a free flowing system, and >0.6 causing a globally jambed system.

```frame_count``` The number of frames in the output GIF. This is also
usually the number of simulation steps that will be run, but that can be
modified via ```--frame-skip```

#### Optional arguments:

```  -h, --help```            show this help message and exit

```  --frame-skip FRAME_SKIP```
The number of spaces that the cells should move in each frame. To
increase the number of simulation steps in the output GIF, it is a good
idea to use this in conjunction with ```--frame-count``` so that fewer
frames need to be rendered (see Warnings). However this will increase
simulation processing time.

```  --cell-size CELL_SIZE``` The number of pixels high and wide each
cell will be rendered as. Increasing this number will increase the size
of the GIF, and excessive cell sizes can cause imagemagick to crash
(see Warnings)


## Warnings

Attempting to generate excessively large GIFs will usually cause
imagemagick to crash.