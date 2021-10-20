# AutoOrg

Do you have lots of unsorted files? Do they group into similar name clusters?

If so, AutoOrg may be the tool for you!

This is a tool that does heuristic sorting of files by similar names into appropriately named directories. It can also sort files into already existing folders as well.

Turn ![unsorted files](readme_images/unsorted_files.png) into ![this](readme_images/sorted_1.png) with 5 clicks.

![how to](readme_images/sorting_1.png)

------

This is a handy tool that is actually the project that provided my initial motivation to learn python back in ~2008! It started out as a WxWidgets GUI back on python 2.5. It has a few somewhat anachronistic architecture decisions for that reason. Since this used to be 32-bit, and I wanted to use it to sort *extremely large* sets of files (20K+), it can use memmapped files for storing the similarity comparison structures. This let me work around the limitations of 32-bit process memory. It also doesn't have a proper UI/worker thread isolation, so running a comparison on lots of files can cause the UI to lag a bit. Fixing this is definitely on my todo list, buteven as-is it's quite handy.

It has just been almost completely rewritten, and now uses Qt as the UI framework, with a *much* better similar file tree view. There are still a few minor warts, but it's useful enough that I'm publishing an actual release.

ToDo:
 - Move file comparison work into a background thread.
 - Get rid of numpy dependency
