# Installation

This is a Python 3 application and requires version 3.2 or greater.

This package can be installed with pip, which comes along with Python 3.4 and above. If downloading from this 
repository, you will need to build the distribution and then install it locally:

`python3 setup.py sdist --formats=zip`

This will create a `dist` folder in the base directory and in it you will find a file called `RetroBrowser-0.1.zip`.

Copy `RetroBrowser-0.1.zip` to a temporary location where you can unzip it. The unzipped folder still needs
to be installed. To install, make sure you are in the directory containing `RetroBrowser-0.1.zip` and execute:

`pip3 install -e RetroBrowser-0.1`

# What is RetroBrowser?

I think there's language framework explosion these days. There's a runaway of escalation of processor and bandwidth
requirements for modern apps. Our computers, phones, and network connections are orders of magnitude faster than they
were 15 years ago, but sites are still slow; apps lag.

RetroBrowser is a super-lightweight proof-of-concept framework that uses the same specification as a web-app 
model-view-controller framework to create a desktop framework for the command line. 

It's a low-tech implementation of Grails... written in Python. For RetroBrowser, I looked at Grails as if it 
were a “specification” rather than an implementation. For this early version, I subtracted the requirement to render 
HTML and instead let views be rendered as plaintext. A sample app, TicTacToe, has been implemented. The game is 
played by entering URL's and query strings at the command prompt.

# Apps

RetroBrowser is an mvc framework; it doesn't do anything by itself.

To see it do something, you'll have to install an app to run on it:

* [TicTacToe](https://github.com/allisonf/tic-tac-toe)

# What major feature is in the pipeline for the 0.2 release?

Whitelisting URLs for improved endpoint security. [ConventionCrawler](https://github.com/allisonf/convention-crawler)
it under development to crawl a RetroBrowser app and programmatically determine it's valid endpoints from the
controllers and actions it finds.

# How Does it Work?

The retrobrowser package stands alone as a framework that will run separate "application" packages. It is the analog of the
Grails framework. The [tictactoe](https://github.com/allisonf/tic-tac-toe) package is the analog of what a developer writes 
when they write a Grails application.

There are some design decisions that make more sense in Groovy than in Python. Notably, the decision to inject the
controller return data into the View classes instead of just passing it in to get_content as an argument is for two
reasons: (1) to match Grails behavior (2) in Groovy, you would not need to do self. so you can reference the injected
variables directly. e.g. board instead of self.board.

* retrobrowser.framework.builder: This is an implementation of the Builder design pattern for Controller objects, View objects, and
action method objects. As configuration, it takes the package, controller, action names parsed from the "url" and the
dictionary parsed from the query string. It translates the names into module, class, and method names, changing
capitalization and adding underscores to convert from the standard for urls to the standard for Python. When the
Controllers are built, Flash and params from the query string are injected into them. The redirect method is also
injected into Controllers to mimic the behavior of redirect in Grails (to allow an action to redirect to another
action).

* retrobrowser.framework.flash: This is a simple module that represents the Flash memory in a Grails application. It outputs error
and message messages to the user. In Grails, these are "flashed" in a box on the page. Controllers each have a Flash and
can write to it. The Flash knows how to "render" (return as a string) its contents.

* retrobrowser.framework.retrobrowser: This module performs the main logic of the framework. It parses command line input, calls the
builder class to get the controllers, views, and actions, calls the action method, and renders (prints) the output
of the View combined with the Dictionary (equivalent to a Groovy Map).

* retrobrowser.framework.inputparser: This class has methods for parsing the url and query string. When the query string is parsed, if
it is ill-formed, a 400 error is thrown by setting the builder's package/controller/action to be those of the framework's
400 Controller and View.

* bin/retroBrowser: This simple script gets the package name from command line input and kicks of the GrailsText main_loop.


# Testing
doctest is used. To run all tests, execute
`python3 tests/retrobrowser.py`