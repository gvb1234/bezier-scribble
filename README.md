# Summary

A perl+gtk3 / python3+gtk3 app to vectorize scanned simple drawings using nice looking Bezier curves.

# Description

With this app, you can draw nice looking (=pdf vector graphics with Bezier curves) paths by specifying (=clicking) on points in a canvas.

The idea is to vectorize a scan of a simple picture drawn with a (black) pencil. So you would open a png file, click a few points for each pencil stroke, and you would get a nice looking vector pdf with the same picture.

There are two types of paths: open and closed path. A path has a starting point and an endpoint (=start for closed path), hence paths also have a direction (from start to end).

The paths have two conditions:

1. be smooth (actually, C<sup>2</sup>).
2. go through the selected points

for more on this, see the Docs folder and/or the wiki.

You can (obviously) add paths to an existing picture.

You can add, move or remove points to existing paths.

You can mark a segment between consecutive points to be black or white (=transpartent) by selecting the appropriate tool, then clicking on the starting point of the segment.

There is no undo (but you can remove points from paths in case of mistake).

When you "export", it will create a pdf file and open it (in the KDE pdf viewer okular in linux, in the default pdf viewer in windows).

Paths look the nicest when their points are equispaced. To best achieve this, the app looks for the maximum intensity point at the edge of a "predicting" cone extending on the (rough) direction of the existing path. This max intensity point is marked in gray. If you click on (or near) it, it will become the next point of the current path.

The radius and opening of the predicting cone can be adjusted by sliders on the side of the main window.

# Background

I did this a long time ago. My young daughter would always ask (bug) me to print "coloring" pages from the internet. These often come in poor quality (lotsa pixels can be seen). So I wanted to replace them with vector graphics curves. It turns out the mathematics of Bezier curves for doing this is fun.

Also, up to that point, I had never written a GUI app, so I wanted to learn. I have no idea why I did it in perl+Gtk2 (at the time) and not in python, but, here it is, finally ported to Gtk3 and significantly cleaned up.

# Update

I ported this to python3 a while ago. Code is much cleaner in python...

# ToDo

Something I always wanted to do is to pick colors from the original file to draw the lines and/or fill the curves/polygons. Part of the code is there (the color picker, for instance). I never found the time to do it though.
