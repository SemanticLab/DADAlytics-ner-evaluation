import json, glob, csv
import requests
import os.path


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


tools = ["spotlight","stanford","nltk","spacy","opener","parsey"]

for directory in glob.glob('data/*'):
	print('Working ', directory)
	data_name = directory.replace('data/','')


	text = open(directory+'/text.txt', encoding="utf-8").read()
	text_lines = text.split('\n')
	text_data = chunks(text_lines,10)
	text_data_blocks = []


	for block in text_data:
		text_block = "\n".join(list(block))
		text_data_blocks.append(text_block)

	
	
	for t in tools:

		data = {}

		print("\t",t)
		out_file_name = directory+'/results_'+t +'_'+data_name+'.json'

		if os.path.isfile(out_file_name):
			continue

		for text_block in text_data_blocks:

			if text_block.strip() == '':
				continue 

			print('----')
			print(text_block)
			print('----')

			try:
				r = requests.post('https://nerserver.semlab.io/compiled', json={"text": text_block, "tool":[t]})

				
			except Exception as error:
				print('-->',r.text,'<--')
				print("error on this one!!!!!")
				continue

			try:
				results = r.json()
				print(results)
			except Exception as error:
				pass

			for result in results['results']:			
				if result not in data:
					if 'typeMode' in results['results'][result]:
						results['results'][result]['typeMode'] = [results['results'][result]['typeMode']]

					data[result] = results['results'][result]
				else:
					if 'typeMode' in results['results'][result]:
						if results['results'][result]['typeMode'] not in data[result]['typeMode']:


							data[result]['typeMode'].append(results['results'][result]['typeMode'])


		json.dump(data,open(out_file_name,'w'),indent=2)




	# console.log(data)

	# for json_file in glob.glob(directory+'/*.json'):

	# 	json_data = json.load(open(json_file))
	# 	print(json_data)
