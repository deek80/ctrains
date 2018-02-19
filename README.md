# C-Trains Programming Problem

The examples from this README are encoded into the tests. In order to run
the tests, you must have Python 3 and pytest. You can install pytest with:
```
pip install pytest
```
and run from this directory (i.e. the one containing this README) with:
```
py.test -v
```

Otherwise, any Python 3 interpreter should be able to use `graph.py` to
build a graph and compute the various properties related to the problem below.


# Background

Calgary is expanding its train service with one-way routes
between various stations. This program is intended to provide
customers with information about the routes, including:
- the distance along certain routes
- the number of different routes between two stations
- the shortest route between two stations

Suppose our routes were as follows:

Departing Station | Arrival Station | Distance (km)
 --- | ----- | ----
 A   |   B   |   5
 B   |   C   |   4
 C   |   D   |   8
 D   |   C   |   8
 D   |   E   |   6
 A   |   D   |   5
 C   |   E   |   2
 E   |   B   |   3
 A   |   E   |   7

The program must be able to compute the following:
1. The distance along the route A-B-C (9)
1. The distance along the route A-D (5)
1. The distance along the route A-D-C (13)
1. The distance along the route A-E-B-C-D (22)
1. The distance along the route A-E-D (no such route)
1. The number of routes starting at C and ending at C with at most 3 stops (2)
1. The number of routes starting at A and ending at C with exactly 4 stops (3)
1. The distance along the shortest route from A to C (9)
1. The distance along the shortest route from B to B (9)
1. The number of different routes from C to C with a distance of less than 30 (7)

(For the "number of routes" and "shortest routes" examples, ignore the 0-length routes!)
