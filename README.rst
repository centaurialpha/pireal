.. |test| image:: https://travis-ci.org/centaurialpha/pireal.svg?branch=master
    :target: https://travis-ci.org/centaurialpha/pireal

.. |issues| image:: https://img.shields.io/github/issues/centaurialpha/pireal.svg?
    :target: https://github.com/centaurialpha/pireal/issues
    :alt: GitHub issues for pireal
    
*****
πreal |test| |issues|
*****

**Pireal** is an educational tool for working with relational database using the query language of relational algebra. *Currently under development*.

.. image:: /src/images/pireal_banner.png

Platforms
#########

* GNU/Linux
* Windows
* Mac OS X

Running
#######

Running from sources

Requirements
************

* `Python 3.x <http://python.org>`_
* `PyQt4 <http://www.riverbankcomputing.co.uk/software/pyqt/intro>`_

Clone the repository:
::

    git clone https://github.com/centaurialpha/pireal.git
    
or download the .zip file and running:
::

    cd pireal
    python pireal.py
    
Syntax
######

- Semicolon at the end of each line is not necessary
- SQL style comments

.. code-block:: sql

    -- This is a comment on Pireal
    -- Other comment

- Valid queries

::

    q1 = people njoin skills
    q2 = select age > 25 (q1)
    q3 = project id, name, skill (q2)

or

::

    project id, name, skill (select age > 25 (people njoin skills))

Implemented Operators
#####################
The operations are implemented in `relation.py <https://github.com/centaurialpha/pireal/blob/master/src/core/relation.py>`_.

+--------------+-----------+
| Operator     | Supported |
+==============+===========+
| Selection    |    Yes    |
+--------------+-----------+
| Projection   |    Yes    |
+--------------+-----------+
| Rename       |    No     |
+--------------+-----------+
| Product      |    Yes    |
+--------------+-----------+
| Union        |    Yes    |
+--------------+-----------+
| Difference   |    Yes    |
+--------------+-----------+
| Natural Join |    Yes    |
+--------------+-----------+
| Intersection |    Yes    |
+--------------+-----------+
| Division     |    No     |
+--------------+-----------+

Demo
####

.. image:: https://github.com/centaurialpha/pireal/blob/gh-pages/img/demo.gif
    :width: 300
    :height: 300
    
Author
######

Gabriel Acosta

* e-mail: acostadariogabriel at gmail
* web: `centaurialpha.githib.io <http://centaurialpha.github.io>`_
* twitter: `@_alfacentauri <http://twitter.com/_alfacentauri>`_
