.. |test| image:: https://travis-ci.org/centaurialpha/pireal.svg?branch=master
    :target: https://travis-ci.org/centaurialpha/pireal
    
:Author: `Gabriel Acosta <http://centaurialpha.github.io>`_

*****
πreal |test|
*****

**Pireal** is a teaching tool for use in learning introduction to database. It allows the user to interactively experiment with Relational Algebra.

.. image:: /src/images/pireal_logo-black.png

Platforms
#########

* GNU/Linux
* Windows
* Mac OS X

Requirements to run/install from source
#######################################
- `Python 3 <http://python.org>`_
- `PyQt5 <http://www.riverbankcomputing.co.uk/software/pyqt/intro>`_
- PyQt5.QtQuick module (package ``python3-pyqt5.qtquick`` in Debian)

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
| Left Outer Join  |    Yes    |
+------------------+-----------+
| Right Outer Join |    Yes    |
+------------------+-----------+
| Full Outer Join  |    Yes    |
+------------------+-----------+
| Intersection     |    Yes    |
+------------------+-----------+
| Division         |    No     |
+------------------+-----------+

Video
#####

.. image:: http://i3.ytimg.com/vi/ks9vUGzMUK0/hqdefault.jpg
   :target: https://youtu.be/ks9vUGzMUK0
