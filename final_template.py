import json
import ast
with open('templates.json', 'r') as file_object:
		contents = json.load(file_object)
dictn = {}
# temp = 0
with open('final_template.txt', 'w') as f,open('dia_acts.txt','w') as g:
	for key, value in contents.items():
		# print type(contents)
	    #print key #gets intent
	    temp= "'"+key+"'"+':['
	    f.write(''.join(temp))
	    g.write(''.join(key))
	    g.write('\n')
	    f.write('\n')
	    # print(type(value))
		# g.write('\n')
	    # key=ast.literal_eval(key)
	    for items,final in enumerate(value):
	    	temp= 'Template('+"'"+final+"'"+'),'
	    	f.write(''.join(temp))
	    	f.write('\n')
	    # f.write('\n')
	    f.write(''.join('],'))
	    
			# # Template('{{ask}}有開哪些課'),
			# print(type(items))
			# print items
			# print '\n ********'
			# for final in items
			# if items not in dictn:
			# 	dictn[items] = {}
			# temp=0
			# for slots,value in final.items():
			# 	# print slots
			# 	# siz = 0
			# 	# if value == 'business':
			# 	# 	print dictn['seat']
			# 	# for i in dictn[items]:
			# 	# 	if i != value:
			# 	# 		siz=siz+1


			# 	if value not in dictn[items].values():
			# 		dictn[items][temp] = value
			# 		temp = temp+1

			# print dictn['seat']
					# print "hhhhhhhhh"
			# dictn[items]=set(dictn[items].items())
			# 	print val
				# f.write(''.join(items))
				# f.write('\n')
				# slot_list.append(items)
			# print items
	# json.dump(dictn,f)
	# print dict
	# f.write('\n')
	# f.write(''.join(slot_list))