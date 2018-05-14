import json, glob, csv
import requests
import os.path


tools = ["spotlight","stanford","nltk","spacy","opener","parsey"]

for directory in glob.glob('data/*'):
	print('Working ', directory)
	data_name = directory.replace('data/','')


	for t in tools:

		in_file_name = directory+'/results_'+t +'_'+data_name+'.json'
		out_csv_name = directory+'/comparison_'+t +'_'+data_name+'.csv'
		ner_data = json.load(open(in_file_name))

		

		markup = json.load(open(directory+'/markup.json'))

		with open(out_csv_name, 'w') as csv_out:




			for markup_entity in markup['entities']:
				exact_match = False
				partial_match = False
				type_match = False
				match_value = ''
				markup_entity['exactMatch'] = ''
				markup_entity['partialMatch'] = ''
				markup_entity['matchValue'] = ''
				markup_entity['typeMatch'] = ''
				# print(markup_entity)
				for ner_entity in ner_data:
					# print(ner_data[ner_entity])
					# print(markup_entity)

					if markup_entity['value'].lower() == ner_data[ner_entity]['text'].lower():
						exact_match = True
						match_value = ner_data[ner_entity]['text']
						markup_entity['exactMatch'] = 'exact'
						markup_entity['matchValue'] = ner_data[ner_entity]['text']

						if 'typeMode' in ner_data[ner_entity]:
							if markup_entity['type'] in ner_data[ner_entity]['typeMode']:
								markup_entity['typeMatch'] = 'true'
								type_match = True

					elif markup_entity['value'].lower() in ner_data[ner_entity]['text'].lower():
						if not exact_match:

							partial_match = True
							markup_entity['partialMatch'] = 'partial'
							markup_entity['matchValue'] = ner_data[ner_entity]['text']						
							match_value = ner_data[ner_entity]['text']
							# pass
							print(markup_entity['value'], ner_data[ner_entity]['text'])
						

			markup['entities'][0]['note'] = ''

			w = csv.DictWriter(csv_out, markup['entities'][0].keys())
			w.writeheader()
			w.writerows(markup['entities'])


		# print(markup)

