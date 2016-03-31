== Installation

This package can be distributed with distutils

`python3 setup.py sdist`

Unzip the resultant file (found in the newly created dist folder) and, from within, execute:

`python3 setup.py install`

== What is RetroBrowser?

RetroBrowser is a console-based, text version of the Grails web framework. Contrary to what you would expect, it is
written in Python, not Groovy. This project was originally designed as the sample Groovy project in the future
Volume 2 of "From Zero to Grails," an introductory Groovy/Grails book.

The grailstext package stands alone as a framework that will run separate "application" packages. It is the analog of the
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


== Testing
doctest is used. To run all tests, execute
`python3 tests/retrobrowser.py`