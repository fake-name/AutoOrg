
import ObjectListView

def itemCleaner(indat):
	if indat == None:
		return ""
	else:
		return "%s" % indat

def initListCtrl(windowPtr):

	windowPtr.fileTree.SetColumns([
		ObjectListView.ColumnDefn("File Name",         "left", 500, valueGetter="fn",  groupKeyGetter="gid"),
		ObjectListView.ColumnDefn("Cleaned Name",      "left", 200, valueGetter="cn",  stringConverter=itemCleaner),
		ObjectListView.ColumnDefn("Similarity Rating", "left", 150, valueGetter="sim", stringConverter=itemCleaner)

	])
	windowPtr.fileTree.CreateCheckStateColumn(columnIndex=0)
	#groupingColumn = windowPtr.fileTree.GetGroupByColumn()
	#print groupingColumn
	#windowPtr.fileTree.SetAlwaysGroupByColumn(groupingColumn)
