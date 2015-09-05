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

Tutorial
########

How to create a database
************************

The database files have the extension ``.pdb (Pireal DataBase)``.

Syntax
******

- The name of the database is the name of ``.pdb`` file.
- To define a table, in the first row must place the name followed fields, like this: ``@relation_name:field1,field2``.
- The tuples separated by commas.

Example of a ``database.pdb`` file:

::

    @people:id,name,age
    001,Mike,15
    002,Gabriel,24
    003,Linus,45
    @skills:id,skill
    002,Python
    003,Linux

The result:

**people**

+---------+---------+---------+
| id      | name    |     age |
+=========+=========+=========+
| 001     | Mike    | 15      |
+---------+---------+---------+
| 002     | Gabriel | 24      |
+---------+---------+---------+
| 003     | Linus   | 45      |
+---------+---------+---------+


**skills**

+-------+-------+
| id    | skill |
+=======+=======+
| 002   | Python|
+-------+-------+
| 003   | Linux |
+-------+-------+

How to create a table/relation
******************************

The table files have the extension ``.prf``, ``csv`` or ``txt``.

Syntax
******

- In ``CSV (comma-separated-values)`` format.
- The first row corresponds to the fields.

There are two ways to create a relationship or table:

- From the menu: ``Relation/Create a Relation`` (Previously created database).
- Or creating a file.


Example:

**skills.prf**

::

    id,skill
    23,Linux
    7,GNU
    6,Gamer
    1,Python
    9,Chef


Now you can load the relation from the menu ``Relation/Load Relation``.

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
