import csv
import json
import operator
import os
import textmining

def obtain_data():
	#with open('sample_train.json') as json_data:
	with open('train.json') as json_data:
	    data = json.load(json_data) # has unicode

	init_dict = {}
	final_dict = {}

	for data_value in data:
		# replace hyphens and other symbols with with empty
		ingredients = [entry.replace(' ', '') for entry in data_value["ingredients"]]
		ingredients = [entry.replace('-', '') for entry in ingredients]
		ingredients = [entry.replace('.', '') for entry in ingredients]
		ingredients = [entry.replace('/', '') for entry in ingredients]
		ingredients = [entry.replace('\\', '') for entry in ingredients]
		ingredients = [entry.replace(')', '') for entry in ingredients]
		ingredients = [entry.replace('(', '') for entry in ingredients]
		new_ings = []

		#removing unicode

		for ingredient in ingredients:
			new_ings.append(ingredient.encode('ascii', 'ignore'))
		if not data_value["cuisine"] in init_dict:
			init_dict[data_value["cuisine"]] = new_ings
		else:
			init_dict[data_value["cuisine"]] += new_ings
		values = ' '.join(init_dict[data_value["cuisine"]])
		#print values
		final_dict[data_value["cuisine"]] = values
		#print type(init_dict[data_value["cuisine"]])

	return final_dict

def obtain_ing_data():
	#with open('sample_train.json') as json_data:
	with open('train.json') as json_data:
	    data = json.load(json_data) # has unicode

	ing_dict = {}

	for data_value in data:
		# replace hyphens and other symbols with with empty
		ingredients = [entry.replace(' ', '') for entry in data_value["ingredients"]]
		ingredients = [entry.replace('-', '') for entry in ingredients]
		ingredients = [entry.replace('.', '') for entry in ingredients]
		ingredients = [entry.replace('/', '') for entry in ingredients]
		ingredients = [entry.replace('\\', '') for entry in ingredients]
		ingredients = [entry.replace(')', '') for entry in ingredients]
		ingredients = [entry.replace('(', '') for entry in ingredients]

		new_ings = []

		#removing unicode

		for ingredient in ingredients:
			new_ings.append(ingredient.encode('ascii', 'ignore'))

		ing_dict[data_value["id"]] = new_ings
		values = ' '.join(ing_dict[data_value["id"]])
		ing_dict[data_value["id"]] = values
	
	return ing_dict

def termdoc(dicto):
	docs = []
	cuisines = ['id']

	# dicto is data

	for entry in dicto:
		docs.append(dicto[entry])
		cuisines.append(entry.encode('ascii', 'ignore'))

	# docs are the sentences

	tdm = textmining.TermDocumentMatrix()

	for doc in docs:
		tdm.add_doc(doc)

	#tdm.write_csv('matrix.csv', cutoff=1)
	length = 0
	num_rows = 0
	matrix_file = 'matrix.csv'

	# remove if file already exists
	try:
		os.remove(matrix_file)
	except OSError:
		pass

	for row, cuisine in zip(tdm.rows(cutoff=1), cuisines):
		with open(matrix_file, 'ab') as csvfile:
			writer = csv.writer(csvfile)
			writer.writerow([cuisine] + row)
		#print [cuisine] + row
		length = len(row)
		num_rows += 1

	# calculating top 10 ingredients

	sum_row = [0] * (length + 1)
	ing_row = []
	for row_index, row in zip(range(num_rows), tdm.rows(cutoff=1)):
		if row_index > 0:
			for index, element in zip(range(length), row):
				sum_row[index] += element
		else:
			ing_row = row

	#print [0] + sum_row
	#print ing_row
	ing_dict = {}

	for ing_name, max_elt in zip(ing_row, sum_row):
		ing_dict[ing_name] = max_elt
		#print ing_name + ': ' + str(max_elt)

	sorted_list = sorted(ing_dict.items(), key=operator.itemgetter(1),
		reverse=True)
	top_ten = sorted_list[0:10]
	print top_ten
	top_ten_file = 'top10ings.csv'

	# fill top 10 ingredients in csv file
	# remove if file already exists
	try:
		os.remove(top_ten_file)
	except OSError:
		pass

	with open(top_ten_file, 'ab') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(['ingredient', 'frequency'])

	for ingredient in top_ten:
		with open(top_ten_file, 'ab') as csvfile:
			writer = csv.writer(csvfile)
			writer.writerow(ingredient)

termdoc(obtain_data())