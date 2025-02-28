# 52CardEngine



## What is the 52CardEngine?

The 52CardEngine is a Python project that uses PyGame to create/render/manage a standard 52 card deck of playing cards. All cards and other visuals
are created with basic geometry using pygame.draw calls. I wanted to build something to let me implement various card games I enjoy playing but
in a video game format, and I figured I'd share the results online for anyone looking to do the same.

## Credits

I provided an example card game in scoundrel.py to demonstrate how the 52CardEngine can be utilized. I do not own any rights to "Scoundrel" (the card game) itself.

The example game is playable [here](https://xerako.itch.io/scoundrel) on itch.io.

"Scoundrel" is a single player Rogue-like Card Game created by Zach Gage and Kurt Bieg. All rights and ownership of "Scoundrel" belong to Zach Gage and Kurt Bieg.
This game is simply implementing their table-top rules into a video game format.

Please see the official rules of "Scoundrel" [here](http://www.stfj.net/art/2011/Scoundrel.pdf).

## Python/Library Versions Used

- Python *3.12.8*
- pygame-ce *2.5.3*
- moderngl *5.12.0*
- glcontext *3.0.0*

Note: moderngl and glcontext are used to render the scoundrel.py example and are entirely just for visual flavor (the background,
text outlines, and drop shadows are all GPU rendered). If this is problematic, you can remove the "renderer" related object and calls
entirely and simply call pygame.display.flip() instead.

## Using this Code

You are free to use the 52CardEngine for whatever personal and commercial purposes you want, with the exception of scoundrel.py ("Scoundrel" is owned
by Zach Gage and Kurt Bieg. The implementation in scoundrel.py is a one-to-one implementation of "Scoundrel," the rights to its rules and game design
are reserved by the original designers).

Xerako