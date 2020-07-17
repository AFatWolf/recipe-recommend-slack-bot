# How to use cookpad.py
0. Open the terminal/cmd, import the needed package:
```
pip install bs4
```
and inside the code, import the cookpad.py:
```
from team.cookpad import *
```
1. Initialize a new object with ingredients list:
```
cookpad = Cookpad(["fish", "onion"])
```
2. `getRecipeLst()` return a recipe list:
```
list = cookpad.getRecipeLst()
```
3. Working ...