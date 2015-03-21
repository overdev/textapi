#textapi

A basic python api for multiline text edition.

`textapi` module was created as part of a personal project, a python/pygame based text editor. It contains the `StrList` class wich holds the text to be edited and  performs (almost) all operations of a visual text box. It also contains the `Caret` class that hold all enumerated operation constants and serves as a caret of `StrList` objects.

###Things `textapi` can do:
A `Strlist` object performs text operations for the following keyboard commands:
   * <kbd>UP</kbd>, <kbd>DOWN</kbd>, <kbd>LEFT</kbd>, <kbd>RIGHT</kbd> to move caret to previous or next column or line;
   * <kbd>HOME</kbd>, <kbd>END</kbd> to move the caret to the beginning and end of line respectively;
   * <kbd>CTRL + <arrow key></kbd> to move the caret horizontaly word by word or scroll the text vertically;
   * <kbd>CTRL</kbd> + (<kbd>HOME</kbd> or <kbd>END</kbd>) to move the caret to the beginning or end of the text;
   * <kbd>BACKSPACE</kbd>, <kbd>DELETE</kbd> to delete the character at the left or right of the caret;
   * <kbd>CTRL</kbd> + (<kbd>BACSPACE</kbd> or <kbd>DELETE</kbd>) to delete the word at the left or right of the caret;
   * Many more.

###TODOs:
* implement text selection operations;
* add copy/paste support;
* add find/replace functionality;
* add save/load of text files and
* some basic code optimizations.

###Things `textapi` *can't* do:
- `textapi` offers no functions for visual rendering or `StrList` objects;
- `StrList` objects are not font or input-method aware; it does not take the character dimensions into account when the caret moves and does not care about what/how text is being typed in.

###Try it out with pygame
If you have [pygame] installed, you can try the **example.py** wich demonstrates how `textapi` can be used.

[pygame]: http://www.pygame.org/wiki/about
