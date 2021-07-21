#!/usr/bin/env python3
import argparse
import csv
import json
from lxml import etree

from eadDocument import EAD

def set_args():
	parser = argparse.ArgumentParser()
	parser.add_argument(
		'-i','--inputPath',
		help='path path to EAD XML file',
		required=True
		)
	parser.add_argument(
		'-m','--mode',
		choices=['items','replace'],
		default='items',
		help=(
			"Choose from:\n"
			"items (return a CSV including item/folder-level units and their respective system IDs)\n"
			"replace (given a CSV of what to replace and under what condition, find and replace with supplied value, "
				"i.e. 'replace value x with y where id==z'\n"
				"See the example replace.csv for help.\n"
				"Note that this will create a new CSV file with '_new' appended to the filename."
			),
		required=True
		)
	parser.add_argument(
		'-r','--replaceCsvPath',
		help=(
			'Path to CSV file with parameters to replace.'
			)
		)

	return parser.parse_args()

def get_id_and_items(main_ead):
	main_ead.get_items()

	with open('items-and-ids.csv','w+') as f:
		writer = csv.writer(f)

		for k,v in main_ead.items.items():
			row = []
			row.append(k)#.replace('aspace','cbpf'))
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

def replace_something(main_ead,replaceCsvPath):
	outpath = main_ead.filepath.replace('.xml','_new.xml')
	print(outpath)
	with open(replaceCsvPath,'r') as f:#, open('out.xml','w+') as o:
		reader = csv.reader(f)
		next(reader, None)

		ead_tree = main_ead.tree

		for row in reader:
			target_xpath = row[0]
			condition_value = row [1]
			replacement_value = row[2]
			target_xpath = target_xpath.replace("VALUE",condition_value)

			target = ead_tree.xpath(target_xpath,namespaces=main_ead.XPATH_NS_MAP)
			print("This is the result of your XPATH expression (it shouldn't be an empty list!):")
			print(target[0])
			try:
				if target[0].is_attribute:
					attribute = target[0].attrname
					tag = target[0].getparent()
					tag.attrib[attribute] = replacement_value
			except:
				pass
			try:
				target[0].text = replacement_value
			except:
				pass

			# target[0] = 'bob'#.getparent().attrib['{http://www.w3.org/1999/xlink}href'] = 'bob'
			# now update the value
			# print(target[0].is_attribute)
			# print(target[0].getparent().attrib)
			# print(ead_tree.xpath(target_xpath,namespaces=main_ead.XPATH_NS_MAP))

		ead_tree.write(outpath)

def main():
	args = set_args()
	main_ead = EAD(args.inputPath)
	if args.mode == 'items':
		get_id_and_items(main_ead)

	if args.mode == 'replace' and args.replaceCsvPath != None:
		replace_something(main_ead,args.replaceCsvPath)
	else:
		print("You need to specify the CSV with the replacement parameters. Try Again!")

if __name__ == "__main__":
	main()
