# Muser

------

## Introduction

This is a musical game which is made using [pyxel](https://pypi.org/project/pyxel/) and [pygame](https://pypi.org/project/pygame/).

## Requirements

+ [pyxel](https://pypi.org/project/pyxel/)
+ [pygame](https://pypi.org/project/pygame/)
+ [mido](https://pypi.org/project/mido/) (For sheet generation)

## Installation

```bash
git clone https://github.com/Qiufeng54321/muser
cd muser
pyxelpackager main.py
```

And then you can find the executable in the dist/ folder.  
Or, you can just run *main.py* without packaging it.

## How to play

### Intro

Click Enter to skip the intro

### Sheet Selection
The sheets are detected in [muser/assets/sheets/](muser/assets/sheets/).  
You can select sheets using left and right arrow keys.  
For every sheet, there are selections of hardness level. You can use up and down arrow keys to change the level.  
Press Space to start the playthrough.

### PlayThrough

+ You can see that there are three rings: red, blue and purple rings.  
+ There are arrows during playthrough, coming from four directions: up, down, left, right.  
+ The arrows move toward the center(where the rings are).  
+ The player has to touch the corresponding key(arrow keys) at the exact time or the arrows will be missed

> + If the note is in the red ring when pressed, it will be a **perfect** note
> + If the note is not in the red ring but the blue one, it will be a **great** note
> + If the note is not in the blue ring but in the purple ring, it will be a **bad** note
> + If the note has passed the rings but the player hasn't pressed the corresponding key yet, then the note will be indicated as **MISS**
>
+ The *total score* is **100000**.
+ There is a weight for each indicator:
>
> + **perfect**: 3
> + **great**: 2
> + **bad**: 1
>
+ For each note pressed by the player, the score will be increased by:  

> + scoreToAdd = 100000 / (weight * noteCount)
>
### Result

The player gets various grades in different ranges of score percentage:  
S: score >= 95  
A: 90 <= score < 95  
B: 80 <= score < 90  
C: 70 <= score < 80  
D: 60 <= score < 70  
F: 0 <= score < 60  
The grade is shown in the center of the screen.  
There are counters of **perfects**, **greats**, **bads**, and **misses** under the grade.  
Press **Enter** to return to the sheet selection cast.
