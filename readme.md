[![Build Status](https://travis-ci.org/ddorn/GUI.svg?branch=release)](https://travis-ci.org/ddorn/GUI)
[![Pypi Version](https://img.shields.io/pypi/v/PygameGUILib.svg)](https://pypi.python.org/pypi/PygameGUILib)
[![Pypi Status](https://img.shields.io/pypi/status/PygameGUILib.svg)](https://pypi.python.org/pypi/PygameGUILib)
[![Python Version](https://img.shields.io/pypi/pyversions/PygameGUILib.svg)](https://pypi.python.org/pypi/PygameGUILib)

[![Code Health](https://landscape.io/github/ddorn/GUI/master/landscape.svg?style=flat)](https://landscape.io/github/ddorn/GUI/master)
[![Pypi Downloads](https://img.shields.io/pypi/dw/PygameGUILib.svg)](https://pypi.python.org/pypi/PygameGUILib)

# Pygame GUI

### What is it ?
 This librairy aims to provide simple widget to improve pygame applications like buttons, text, textboxes or 
 math text widgets. There is also some goemetric shapes, like rectangle or bezier curves.

### Dependancies
* **pygame :**   This library is fully based on pygame, so you must have it installed.

*(optionnal)*
* **latex :** you must avec latex install if you want to use the `LaText` widget 
            (`latex` and `dvipng` accessible in path)

### Installation
 You can install it with pip and pypi easily by :
        
    pip install -U PygameGUILib
    
 or via git and pip : 
 
    pip install -U git+https://github.com/ddorn/GUI.git@release#egg=GUI    

### Widgets

Actually there is a fex widgets in the library. I'll try to maintain this list, but I'm sure I'll forget, 
so there is *MORE* than that.

 * Texts :
    * SimpleText
    * LaText
    * InLineInputBox
    * InLinePassBox
 * Buttons :
    * Button
    * IconButton
    * SlideBar

Around that, there is a lot of helping objects, like `Font`, colors, `V2` and `Separator` (some vector things), 
FPSIndicator, FocusSelector...
 

### Use

##### Bases
Every widget has a `pos`, a `size` and an `anchor`, the three can be harcoded or a callback function with no parameters.
The `pos` and the `size` defines a `pygame.Rect` where the widget is. The `pos`is per default the center of the widget, 
but you can change this behavior by giving an other `anchor`, like `TOPLEFT`. 

##### Tree steps to use a button


Every widget is totally independent and will do nothing unless you tell him to do something.
There is no theading thing that continuously check for events both for performance and to give you more 
control on the widgets.

For instance, widget won't auto-render on the screen and won't listen events, like clics on buttons.  
Thus, to have a fully operational button there are three steps :

Just define it, nothing complex once you've read the bases.

    # define the action the button will perform when clicked
    def callback():
        print('PRESSED !")
        
    button = Button(callback, (100, 100), (100, 40), "Click Me !")

Then, you must continuously check for events, and call `click()` when you want. 
(typically when the user clicks the button)

    for e in pygame.events.get():
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:  # left click
            if pygame.mouse.get_pos() in button:
                button.press()  # you tell the button to call the callback if clicked

And finally you must render the button on the screen.
                    
     button.render(display)  # you draw the button on the display

It's basically the same thing for any widget, except for "passive" widgets like texts, because 
we do not bother if the user clicks it. For other widgets, like textboxes, you'll want to update them with the inputs
so you must call `.update(event)` too.

##### Limitations

 As always with pygame, do not try to make too big apps with a lot of changing texts or with too big protions of the screen
 that are too often redrawn or it can lag a bit. 

### Help and todo list

You're welcome ! 

###### How can you help ?
 Do not hesitate to [contact me per mail](mailto:diego.dorn@free.fr) 
 or [join the slack chat](https://join.slack.com/pygamegui/shared_invite/MTk5NDY0Njg4MTE1LTE0OTc4MDcwMzYtYWU5Mjc4ZjA1ZA)
 to discuss aboute code, optimisation or functionnalities. 
 You can of course make any push request you want !  
 Feel free to report any issue you see as I do not have strong tests (I mean, almost no tests !)
 

###### Todos : 
 * A `Text` class to make texts that goes on more lines and with wrapping.
 * A `TextBox`, to input multi line text
 * A `RichText` to make text with differents inner colors/size/font/styles
 * Something like lists
 * `Switch` class : Nice looking ON/OFF button
 * Some geometry function to draw curves, grids and manipulate line, polygons
 
 This is absolutly not an ordered list, they will come as I have nice looking and useable classes !
 

### Cool projects with this library

Do not hesitate to tell me if you have something working !  
Here is a list of projets that uses my library, take inspiration !

 * [**Crabes**](https://github.com/ddorn/crabes) : a simulation too for a [TFJM²](https://www.tfjm.org/) problem
 * Your project !
 
Examples at the and of each file can also give you a lot of samples of how to use this library :)
There is also a folder full of example that you *will* apreciate !
