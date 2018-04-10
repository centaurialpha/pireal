.. |travis| image:: https://travis-ci.org/centaurialpha/pireal.svg?branch=master
    :target: https://travis-ci.org/centaurialpha/pireal
.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/d9wa6whp1fpq4uii?svg=true
    :target: https://ci.appveyor.com/project/centaurialpha/pireal
    
:Author: `Gabriel Acosta <http://centaurialpha.github.io>`_

*****
πreal |travis| |appveyor|
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

.. image:: http://i3.ytimg.com/vi/np4h-Q1aMBg/hqdefault.jpg
   :target: https://www.youtube.com/watch?v=np4h-Q1aMBg

Donate
##########
I hope Pireal was useful. You can donate any amount that you think Pireal deserves.

.. image:: https://www.paypalobjects.com/es_XC/AR/i/btn/btn_donateCC_LG.gif
   :target: https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=29STPF8BWWUTY
