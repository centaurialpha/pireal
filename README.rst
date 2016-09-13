.. |test| image:: https://travis-ci.org/centaurialpha/pireal.svg?branch=master
    :target: https://travis-ci.org/centaurialpha/pireal

:Author: `Gabriel Acosta <http://centaurialpha.github.io>`_

*****
πreal |test|
*****

**Pireal** is a teaching tool for use in learning introduction to database. It allows the user to interactively experiment with Relational Algebra

.. image:: /src/images/pireal_logo-black.png

Platforms
#########

* GNU/Linux
* Windows
* Mac OS X

Requirements to run/install from source
#######################################

* Python 3
* PyQT5.Qt.Quick
(package `qml-module-qtquick2` in Debian)

Implemented Operators
#####################
The operations are implemented in `relation.py <https://github.com/centaurialpha/pireal/blob/master/src/core/relation.py>`_.

+------------------+-----------+
| Operator         | Supported |
+==================+===========+
| Selection        |    Yes    |
+------------------+-----------+
| Projection       |    Yes    |
+------------------+-----------+
| Rename           |    No     |
+------------------+-----------+
| Product          |    Yes    |
+------------------+-----------+
| Union            |    Yes    |
+------------------+-----------+
| Difference       |    Yes    |
+------------------+-----------+
| Natural Join     |    Yes    |
+------------------+-----------+
| Left Outer Join  |    No     |
+------------------+-----------+
| Right Outer Join |    No     |
+------------------+-----------+
| Full Outer Join  |    No     |
+------------------+-----------+
| Intersection     |    Yes    |
+------------------+-----------+
| Division         |    No     |
+------------------+-----------+

Video
#####

.. image:: http://img.youtube.com/vi/UkfJpu6YlVM/hqdefault.jpg
   :target: https://www.youtube.com/watch?v=UkfJpu6YlVM
