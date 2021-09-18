# Knuth algorithm visualisation improvements

This program is tested version of the implementation of the Knuth algorithm, an algorithm used within the proccess of edge profiling. The program itself is work of our colleageus David Gavrilović and Nikola Dimić that can be found on this [link] (https://github.com/MATF-Software-Verification/2019_05_Knut_profajliranje_ivica_vizuelizacija). Algorithm has been improved with the following:

* All the functions that are used for creating CFG and spanning tree are tested (errors are fixed)
* Previous code only supported the predefinded input, now you can select from our collection or write your own code file
* It supports any input with manual adding of the initial weights (weights are incremented by double clicking on the weight of an edge)
* Visualisation of a graph is improved


All of the steps are presented seperately.


 ## :computer: Getting started

 These instructions will help you run and visualise Python code on your local machine. This version is mainly tested on Ubuntu and MacOS.


### Prerequisites

What things you need to install the software and how to install them

Python3 - version 3.6.5
```
$ python3 --version
Python 3.6.5
```

Tkinter
```
$ sudo pacman -S tk
```

## 🔌 How to run

```
python visualise.py
```

1. Choose an example you want to use as a code input (press the button) or write an example
2. Make sure that the code does not log any errors
2. Generate canvas
3. Procceed trough the steps using the next button
4. You can change inverse tree initial weights by double click on them 


## :wrench: Built using
* [tkinter](https://docs.python.org/3/library/tkinter.html) -  Python interface to the Tk GUI toolkit

## :mortar_board: Authors

* **Jovana Bošković** - [jboskovic](https://github.com/jboskovic)

* **Veronika Miljaković** -  [veronika1996](https://github.com/veronika1996)

* **Milica Galjak** -  [milicagaljak](https://github.com/milicagaljak)


## :sunrise: App screenshot

![slika](img/imgStart.png)

![slika1](img/imgEnd.png)
