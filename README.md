# AutoOrg

Do you have lots of unsorted files? Do they group into similar name clusters?

If so, AutoOrg may be the tool for you!

This is a tool that does heuristic sorting of files by similar names into appropriately named directories. It can also sort files into already existing folders as well.

Turn ![unsorted files](readme_images/unsorted_files.png) into ![this](readme_images/sorted_1.png) with 5 clicks.

![how to](readme_images/sorting_1.png)

 - The folder containing files you want to sort goes into the "Directory to process" input. You can also hit the neighboring "select directory" button for a folder picker.
 - If you want to sort into a existing set of directories, enable the "Sort into directory" line.
 - Finally, "Run Sort" loads the filenames, and generates the dense matrix of filename similarity metrics.
 - At this point, you should have some contents in the main tree-view area.
 - The sorting is controlled by the "Similarity grouping threshold" slider. Functionally, starting with one of the files, all names similar to it are greedily grouped into buckets if they are at least "Similarity grouping threshold" similar to the picked name. This continues until all files are either sorted into buckets, or have been examined and no similar names have been fouhd.
 - Most of the buttons on the bottom of the UI are convenience functions. You can check all potential folders with 2-10 items, check or uncheck everything, expand and contract the tree, etc...
 - No files are moved, and no folders created until the "Move selected files into Directory" button is pressed. If "Sort into directory" is disabled, this will open a folder picker for you to chose where to put the newly created directories, into which the files will be moved. If "Sort into directory" is enabled, it will just immediately begin moving files.
 - When "Sort into directory" is enabled, where the files will be moved to is previewed in the "Destination Path" column of the tree view.

------

This is a handy tool that is actually the project that provided my initial motivation to learn python back in ~2008! It started out as a WxWidgets GUI back on python 2.5. It has a few somewhat anachronistic architecture decisions for that reason. Since this used to be 32-bit, and I wanted to use it to sort *extremely large* sets of files (20K+), it can use memmapped files for storing the similarity comparison structures. This let me work around the limitations of 32-bit process memory. It also doesn't have a proper UI/worker thread isolation, so running a comparison on lots of files can cause the UI to lag a bit. Fixing this is definitely on my todo list, buteven as-is it's quite handy.

It has just been almost completely rewritten, and now uses Qt as the UI framework, with a *much* better similar file tree view. There are still a few minor warts, but it's useful enough that I'm publishing an actual release.

ToDo:
 - Move file comparison work into a background thread.
 - Get rid of numpy dependency
