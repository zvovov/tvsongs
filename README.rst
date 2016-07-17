=======
tvsongs
=======
Find and listen to songs featured in TV shows.

.. image:: https://travis-ci.org/zvovov/tvsongs.svg?branch=master
    :target: https://travis-ci.org/zvovov/tvsongs

Highlights:
 * Find `that` song you heard in `that` TV show but couldn't find anywhere.
 * Searching is easy - descriptions are provided for each episode.
 * See songs for a specific season and episode, or see songs in all seasons all episodes in one go.
 * Listen to the song with the YouTube link provided along with it.
 * All song data is collected in real-time, therefore up to date.
 * Runs on Python 3.x. No support for Python 2.x yet.


Requirements
------------
* Python 3
* The python modules listed in `requirements.txt`_. They will be installed automatically:

  * requests
  * beautifulsoup4
  * python-slugify

* A working Internet connection
* Name of a TV show. ;)


Installation
------------

.. code-block::

    $ pip3 install tvsongs


Usage
-----
.. code-block::

    $ tvsongs
     Name of the Show: daredevil

     Searching...

     Daredevil
     Total Seasons: 2

     Season 1    Episode(s): 13    Aired: Apr 2015 to Apr 2015
     Song(s): 26

     Season 2    Episode(s): 13    Aired: Mar 2016 to Mar 2016
     Song(s): 17

     Total Song(s) in Daredevil: 43

     Choose Season of Daredevil. 1 to 2 (0 for all): 0
     ...

All the songs will be listed now.


For quick help::

    $ tvsongs help


Support
=======

If you encounter any bugs, then please `let me know here`_.



License
=======
::

  The MIT License (MIT)

  Copyright (c) 2016 Chirag Khatri

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.


.. _let me know here: https://github.com/zvovov/tvsongs/issues
.. _requirements.txt: https://github.com/zvovov/tvsongs/blob/master/requirements.txt
