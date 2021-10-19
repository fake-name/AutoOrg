

	#def __repr__(self):
	#	return (repr((self.fn, self.cn, self.pairs)))

class ConfigObj(object):
	def __init__(self):
		self.comp_threshold            = 1500

		self.word_length_weighting     = 1000
		self.str_length_weighting      = 1000
		self.word_difference_weighting = 1000

		self.strip_terms               = []
		self.strip_str                 = ""

		self.brackets                  = True
		self.parentheses               = True
		self.curly_braces              = True
		self.duplicate_segments        = True
		self.file_extensions           = True


		self.mapping_dict              = {}
		self.sort_from_dir             = "~/"
		self.sort_to_dir               = ""
		self.enable_sort_to_dir        = True


	def getCompThresh(self):
		return float(self.comp_threshold)/1000

	def dump(self):
		config = {}
		config["enable_sort_to_dir"]        = self.enable_sort_to_dir
		config["sort_to_dir"]               = self.sort_to_dir
		config["sort_from_dir"]             = self.sort_from_dir
		config["comp_threshold"]            = self.comp_threshold

		config["word_length_weighting"]     = self.word_length_weighting
		config["str_length_weighting"]      = self.str_length_weighting
		config["word_difference_weighting"] = self.word_difference_weighting

		config["strip_terms"]               = self.strip_terms
		config["strip_str"]                 = self.strip_str

		config["brackets"]                  = self.brackets
		config["parentheses"]               = self.parentheses
		config["curly_braces"]              = self.curly_braces
		config["duplicate_segments"]        = self.duplicate_segments
		config["file_extensions"]           = self.file_extensions

		return config

	def load(self, config):

		self.enable_sort_to_dir         = config["enable_sort_to_dir"]
		self.sort_to_dir                = config["sort_to_dir"]
		self.sort_from_dir              = config["sort_from_dir"]
		self.comp_threshold             = config["comp_threshold"]
		self.word_length_weighting      = config["word_length_weighting"]
		self.str_length_weighting       = config["str_length_weighting"]
		self.word_difference_weighting  = config["word_difference_weighting"]

		self.strip_terms                = config["strip_terms"]
		self.strip_str                  = config["strip_str"]

		self.brackets                   = config["brackets"]
		self.parentheses                = config["parentheses"]
		self.curly_braces               = config["curly_braces"]
		self.duplicate_segments         = config["duplicate_segments"]
		self.file_extensions            = config["file_extensions"]

		return

	def __setattr__(self, key, value):

		ok_keys = [
			'comp_threshold',
			'word_length_weighting',
			'str_length_weighting',
			'word_difference_weighting',
			'strip_terms',
			'strip_str',
			'brackets',
			'parentheses',
			'curly_braces',
			'mapping_dict',
			'sort_from_dir',
			'sort_to_dir',
			'enable_sort_to_dir',
			'duplicate_segments',
			'file_extensions',
		]
		assert key in ok_keys, "Trying to set invalid key '%s'" % key

		super().__setattr__(key, value)




