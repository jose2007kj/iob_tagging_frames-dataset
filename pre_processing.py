import json
# import nltk
# nltk.download('punkt')
# from nltk.tokenize import wordpunct_tokenize
import re
with open('train1_template.txt', 'w') as f:
	with open('frames.json', 'r') as file_object:
		contents = json.load(file_object)
		for i in range(0,1300):
			print(i, '****************************')
			for item in contents[i]['turns']:
				if 'user' in item['author']:
					#tokens = nltk.word_tokenize(item['text']) 
					#tokens = wordpunct_tokenize(item['text'])
					#print(tokens)
					# print("non-processed",item['text'])
					removed = re.sub(r",\s+", " ", item['text'])#for removing hello, I am also taking care of 23,000
					dot = re.sub(r"\.+", " ", removed)#for removing one or more dots
					
					remov = re.sub(r"\?+", " ", dot)# remove ?
					exc = re.sub(r"\!+", " ", remov)#remove !
					exc =exc.rstrip()
					pattern = re.compile(r'\s+')
					final = re.sub(pattern," ", exc) #for removing extra spaces
					# print("removed commas",removed)
					#print("removed dot",dot) #
					# print("Final",exc)
					# print ("words count is",len(final.split()))
					iob = []
					for k in range (0,len(final.split())):
						if k ==0:
							iob.append("O")
						else:
							iob.append(" O")
					intent = ""
					z=0
					for args in item['labels']['acts_without_refs']:
						# print("intent",args['name'])
						if z ==0:
							intent += args['name']
							z=z+1
						else:
							if args['name'] not in intent:	
								intent += " "+args['name']
								# z=z+1
						for val in args['args']:
							# print("type ",type(val['val']) ,isinstance(type(val['val']), str))
							wc = 0 
							if type(val['val']) == str:
								if 'book' not in val['val']:
									# print("val,key",val['val'],val['key'])
									n_val = re.sub(r",\s+", " ", val['val'])
									print("val",n_val)
									wc = len(n_val.split())
							else:
								print("else val,key",val['val'],val['key'])
								n_val = val['val']
								# if val['key'] in final:
								# print('boolean found***????????????????',val['key'],final)
								pos = 0
								# print("val is",n_val)
								for idx,word in enumerate(final.split()):
									if val['key'] in word:
										pos = idx
										print("position brek",pos)
										break
								# tag = "B_"+val['key']
								# iob[pos] = iob[pos].replace("O", tag)
								if val['key'] in final:
									tag = "B_"+val['key']
									iob[pos] = iob[pos].replace("O", tag)
									print("----------------------------")
									print(iob)
									print(final)
									print("----------------------------")

								wc = 0
							# wc = len(n_val.split())
							if wc == 1:
								pos = 0
								print("val is",n_val)
								for idx,word in enumerate(final.split()):
									if n_val in word:
										pos = idx
										print("position brek",pos)
										break


								# indices = [idx for idx, word in enumerate(final.split(), 1) if n_val in word]
								print(final)
								print("1 word match? ",n_val, pos)
								# res = int(indices)
								# indices = int(indices)
								# print(res)
								tag = "B_"+val['key']
								iob[pos] = iob[pos].replace("O", tag)
								# for x in range(0,len(iob)): #working for loop
								# 	iob[x] = iob[x].replace("O", "nmnmnm")
								# 	print("iob",iob[x])
							elif wc > 1:
								print("more than 1 word",wc)
								for idx,word in enumerate(n_val.split()):
									for idy,word2 in enumerate(final.split()):

										if word in word2:
											pos = idy
											# print("position brek",pos)
											if idx == 0:
												tag = "B_"+val['key']
												iob[pos] = iob[pos].replace("O", tag)
												break
											else:
												tag = "I_"+val['key']
												iob[pos] = iob[pos].replace("O", tag)
												break


							else:
								print("0 words")
					f.write(intent)
					f.write('\n')
					f.write(final +'\n') 
					f.write(''.join(iob))
					f.write('\n')					
					# for act in item['labels']['frames']:
					# 	if 'intent' in act['info']:
					# 		for intent in act['info']['intent']:
					# 			print(intent['val'])
                    		
