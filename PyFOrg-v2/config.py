

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

		self.mapping_dict              = {}
		self.target_dir                = "~/"
		self.sort_to_dir               = ""
		self.enable_sort_to_dir        = True


	def getCompThresh(self):
		return float(self.comp_threshold)/1000

	def dump(self):
		config = {}
		config["enable_sort_to_dir"]       = self.enable_sort_to_dir
		config["sort_to_dir"]              = self.sort_to_dir
		config["target_dir"]               = self.target_dir
		config["compThreshold"]            = self.comp_threshold

		config["wordLengthWeighting"]      = self.word_length_weighting
		config["strLengthWeighting"]       = self.str_length_weighting
		config["wordDifferenceWeighting	"] = self.word_difference_weighting

		config["stripTerms"]               = self.strip_terms
		config["stripStr"]                 = self.strip_str

		config["brackets"]                 = self.brackets
		config["parentheses"]              = self.parentheses
		config["curlyBraces"]              = self.curly_braces

		return config

	def load(self, config):

		self.enable_sort_to_dir         = config["enable_sort_to_dir"]
		self.sort_to_dir                = config["sort_to_dir"]
		self.target_dir                 = config["target_dir"]
		self.comp_threshold             = config["compThreshold"]
		self.word_length_weighting      = config["wordLengthWeighting"]
		self.str_length_weightingconfig = config["strLengthWeighting"]
		self.word_difference_weighting  = config["wordDifferenceWeighting"]

		self.strip_terms                = config["stripTerms"]
		self.strip_str                  = config["stripStr"]

		self.brackets                   = config["brackets"]
		self.parentheses                = config["parentheses"]
		self.curly_braces               = config["curlyBraces"]

		return



