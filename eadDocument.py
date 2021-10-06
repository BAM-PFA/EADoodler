from lxml import etree

'''
This is just the class for the EAD doc with a couple methods to
do stuff:
* extract all the items and their ASpace ids
* more later?
'''
class EAD:
	def __init__(self,path):

		self.filepath = path

		self.tree = etree.parse(path)

		self.XMLNS = "urn:isbn:1-931666-22-9"
		self._EAD = "{{}}".format(self.XMLNS)
		self.XSI_NS = "http://www.w3.org/2001/XMLSchema-instance"
		self.XLINK = "http://www.w3.org/1999/xlink"
		self.SCHEMA_LOCATION = ("urn:isbn:1-931666-22-9 "
			"http://www.loc.gov/ead/ead.xsd")
		# reference for namespace inclusion:
		# https://stackoverflow.com/questions/46405690/how-to-include-the-namespaces-into-a-xml-file-using-lxml
		self.attr_qname = etree.QName(self.XSI_NS, "schemaLocation")

		self.NS_MAP = {
			None:self.XMLNS,
			'xsi':self.XSI_NS,
			'xlink':self.XLINK
			}
		# can't use an empty namespace alias with xpath
		self.XPATH_NS_MAP = {
			'e':self.XMLNS,
			'xsi':self.XSI_NS,
			'xlink':self.XLINK
			}

		self.items = {}

	def get_items(self):
		ead_tree = self.tree
		all_items = ead_tree.xpath(
			'//e:*[starts-with(name(), "c0")][@level="file" or @level="item"]',
			namespaces= self.XPATH_NS_MAP
			)
		# print(len(all_items))

		for item in all_items:
			_id = item.xpath(
			'@id',
			namespaces=self.XPATH_NS_MAP
			)
			# print(_id)
			self.items[_id[0]] = item
