import csv, json


output = {
	"orginalFilename" :"Mary diaries 1903_Danaversion",
	"description" : "Mary Berenson's diary_1903-1904",
	"entities" : []
}
with open ('new_markup.csv') as f:


	reader = csv.reader(f)


	for row in reader:

		output['entities'].append({"type": row[1],"value":row[2],"note":row[3]})



json.dump(output,open('markup.json','w'))

