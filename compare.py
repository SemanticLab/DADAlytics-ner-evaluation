import json, glob, csv
import requests
import os.path


tools = ["spotlight","stanford","nltk","spacy","opener","parsey"]
all_summary = {}


for directory in glob.glob('data/*'):
	print('Working ', directory)
	data_name = directory.replace('data/','')

	# if (directory != 'data/book_night_battles'):
	# 	continue

	all_summary[data_name] = {'tools':{}}



	for t in tools:

		

		in_file_name = directory+'/results_'+t +'_'+data_name+'.json'
		out_csv_name = directory+'/comparison_'+t +'_'+data_name+'.csv'
		out_json_name = directory+'/json_comparison_'+t +'_'+data_name+'.json'


		ner_data = json.load(open(in_file_name))

		ner_data_entities = []
		ner_data_entities_dupe_check = []

		for x in ner_data:

			if ner_data[x]['text'].lower() in ner_data_entities_dupe_check:
				continue

			ner_data_entities_dupe_check.append(ner_data[x]['text'].lower() )
			

			ner_data_entities.append(ner_data[x])

		markup = json.load(open(directory+'/markup.json'))

		with open(out_csv_name, 'w') as csv_out:


			json_results = {'summary':{},'partial':[], 'exact':[], 'noMatch':[], 'file':markup['description']}

			foundTerms = []

			for markup_entity in markup['entities']:

				exact_match = False
				partial_match = False
				type_match = False
				match_value = ''
				markup_entity['exactMatch'] = ''
				markup_entity['partialMatch'] = ''
				markup_entity['matchValue'] = ''
				markup_entity['typeMatch'] = type_match


				for ner_entity in ner_data_entities:


					if markup_entity['value'].lower() == ner_entity['text'].lower():
						exact_match = True
						match_value = ner_entity['text']
						markup_entity['exactMatch'] = 'exact'
						markup_entity['matchValue'] = ner_entity['text']

						if partial_match:
							markup_entity['partialMatch'] = ''

						if 'typeMode' in ner_entity:
							if markup_entity['type'] in ner_entity['typeMode']:
								markup_entity['typeMatch'] = True
								type_match = True
							else:
								markup_entity['typeMatch'] = False
								


					elif (markup_entity['value'].lower() in ner_entity['text'].lower() or ner_entity['text'].lower() in markup_entity['value'].lower()) and len(ner_entity['text'].lower())>3:
						if not exact_match:

							partial_match = True
							markup_entity['partialMatch'] = 'partial'
							markup_entity['matchValue'] = ner_entity['text']						
							match_value = ner_entity['text']

							if 'typeMode' in ner_entity:
								if markup_entity['type'] in ner_entity['typeMode']:
									markup_entity['typeMatch'] = True
									type_match = True
								else:
									markup_entity['typeMatch'] = False
									


				if exact_match:
					json_results['exact'].append({'valueMarkup':markup_entity['value'], 'valueNER':markup_entity['matchValue'], 'typeMatch':markup_entity['typeMatch']})
					foundTerms.append(markup_entity['value'])
				elif partial_match:
					json_results['partial'].append({'valueMarkup':markup_entity['value'], 'valueNER':markup_entity['matchValue'], 'typeMatch':markup_entity['typeMatch']})
					foundTerms.append(markup_entity['value'])

			markup['entities'][0]['note'] = ''

			w = csv.DictWriter(csv_out, markup['entities'][0].keys())
			w.writeheader()
			w.writerows(markup['entities'])


			for markup_entity in markup['entities']:

				if markup_entity['value']  not in foundTerms:

					json_results['noMatch'].append(markup_entity)

	
			json_results['summary']['exactMatches'] = len(json_results['exact'])
			json_results['summary']['partialMatches'] = len(json_results['partial'])
			json_results['summary']['totalMarkup'] = len(markup['entities'])
			json_results['summary']['totalNotFound'] = len(json_results['noMatch'])
			


			all_summary[data_name]['desc'] = json_results['file']



			all_summary[data_name]['tools'][t] = json_results['summary']


			json.dump(json_results,open(out_json_name,'w'))

json.dump(all_summary,open('all_summary.json','w'))

		# print(markup)

