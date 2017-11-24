import csv
import json
import operator
import os
import textmining # Third-party library

# Function to carry out preprocessing on `data`
def preprocessing(data):
	symbols = " -./\\)(,\'!&%1234567890"
	for symbol in symbols:
		data = [entry.replace(symbol, '') for entry in data]

	return data

# Function to obtain the training data as a dictionary
def obtain_data():
	with open('train.json') as json_data:
	    data = json.load(json_data) # has unicode

	init_dict = {}
	final_dict = {}

	for data_value in data:
		# Carry out preprocessing
		ingredients = preprocessing(data_value["ingredients"])
		new_ings = []

		# Removing unicode from all names
		for ingredient in ingredients:
			new_ings.append(ingredient.encode('ascii', 'ignore'))
		if not data_value["cuisine"] in init_dict:
			init_dict[data_value["cuisine"]] = new_ings
		else:
			init_dict[data_value["cuisine"]] += new_ings

		values = ' '.join(init_dict[data_value["cuisine"]])
		final_dict[data_value["cuisine"]] = values

	return final_dict

# Function to obtain the term-document matrix (TDM) using textmining library
# `dicto` is the data
def termdoc(dicto):
	docs = []
	cuisines = ['cuisine']

	# Add data to the TDM and remove unicode from cuisine names
	for entry in dicto:
		docs.append(dicto[entry])
		cuisines.append(entry.encode('ascii', 'ignore'))

	# Use of textmining library to obtain TDM
	tdm = textmining.TermDocumentMatrix()
	for doc in docs:
		tdm.add_doc(doc)

	matrix_file = 'matrix.csv'

	# Remove 'matrix.csv' if it already exists
	try:
		os.remove(matrix_file)
	except OSError:
		pass

	# Write frequencies of all ingredients in each cuisine
	for row, cuisine in zip(tdm.rows(cutoff=1), cuisines):
		with open(matrix_file, 'ab') as csvfile:
			writer = csv.writer(csvfile)
			writer.writerow([cuisine] + row)

termdoc(obtain_data())