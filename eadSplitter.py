#!/usr/bin/env python3
import csv
import json
from lxml import etree
import os
import sys

class EAD:
	def __init__(self,path):

		self.tree = etree.parse(path)

		self.XMLNS = "urn:isbn:1-931666-22-9"
		self._EAD = "{{}}".format(self.XMLNS)
		self.XSI_NS = "http://www.w3.org/2001/XMLSchema-instance" 
		self.SCHEMA_LOCATION = ("urn:isbn:1-931666-22-9 "
			"http://www.loc.gov/ead/ead.xsd")
		# reference for namespace inclusion: 
		# https://stackoverflow.com/questions/46405690/how-to-include-the-namespaces-into-a-xml-file-using-lxml
		self.attr_qname = etree.QName(self.XSI_NS, "schemaLocation")

		self.NS_MAP = {
			None:self.XMLNS,
			'xsi':self.XSI_NS
			}
		# can't use an empty namespace alias with xpath
		self.XPATH_NS_MAP = {
			'e':self.XMLNS
			}

		self.items = {}

	def get_items(self):
		ead_tree = self.tree
		all_items = ead_tree.xpath(
			'//e:*[starts-with(name(), "c0")][@level="file" or @level="item"]',
			namespaces= self.XPATH_NS_MAP
			)
		print(len(all_items))

		for item in all_items:
			_id = item.xpath(
			'@id',
			namespaces=self.XPATH_NS_MAP
			)
			print(_id)
			self.items[_id[0]] = item

def main():
	path = sys.argv[1]
	main_ead = EAD(path)

	main_ead.get_items()

	with open('out.csv','w+') as f:
		writer = csv.writer(f)

		for k,v in main_ead.items.items():
			row = []
			row.append(k.replace('aspace','cbpf'))
			title = v.xpath('string(descendant::e:unittitle)',namespaces=main_ead.XPATH_NS_MAP)
			if title == [] or not title:
				row.append('')
			else:
				row.append(title)
			date  = v.xpath('descendant::e:unitdate/text()',namespaces=main_ead.XPATH_NS_MAP)
			if date == []:
				row.append('')
			else:
				row.append(date[0])
			desc = v.xpath('string(descendant::e:scopecontent/e:p)',namespaces=main_ead.XPATH_NS_MAP)
			if desc == [] or not desc:
				row.append('')
			else:
				row.append(desc)
			print(row)
			writer.writerow(row)

if __name__ == "__main__":
	main()



