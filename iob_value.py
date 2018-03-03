import json
# import nltk
# nltk.download('punkt')
# from nltk.tokenize import wordpunct_tokenize
import re
import numpy as np
import pandas as pd
from pandas import DataFrame, read_csv
with open('train2.iob', 'w') as f:
	with open('frames/frames.json', 'r') as file_object:
		contents = json.load(file_object)
		crf = []
		kj = []
		num = 0
		no_slots = []
		ontology = {}
		onto_key = 0
		boolean = []
		text = []
		df=pd.DataFrame(columns=['nl', 'act1', 'act2', 'act3', 'act4', 'slot1', 'slot2', 'slot3', 'slot4'])
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
					final= final.replace('$',"") #for removing $
					# print("removed commas",removed)
					#print("removed dot",dot) #
					# print("Final",exc)
					# print ("words count is",len(final.split()))
					iob = []
					final = final.lower()
					for k in range (0,len(final.split())):
						if k ==0:
							iob.append("O")
						else:
							iob.append(" O")
					intent = ""
					act = []
					slots = []
					z = 0
					for args in item['labels']['acts_without_refs']:
						# print("intent",args['name'])
						# act.append(args['name'])
						# z=z+1
						if z ==0:
							intent += args['name']
							z=z+1
						else:
							if args['name'] not in intent:	
								intent += " "+args['name']
								z=z+1
						temp = 0
						print("**********************************",len(args['args']))
						if len(args['args']) == 0:
							act.append(args['name'])
							no_slots.append(" "+args['name'])
						for val in args['args']:
							# print("type ",type(val['val']) ,isinstance(type(val['val']), str))
							wc = 0 
							if type(val['val']) == str:
								if 'book' not in val['val']:
									# print("val,key",val['val'],val['key'])
									n_val = re.sub(r",\s+", " ", val['val'])
									n_val = n_val.replace('$', '')
									print("+++++++++++++++++++++",n_val,final)
									# n_val = val['val']
									n_val = n_val.lower()
									print("val",n_val)
									wc = len(n_val.split())
									# slot[temp] = val['key']
							else:
								print("else val,key",val['val'],val['key'])
								n_val = val['val']
								# n_val= n_val.lower()
								# if val['key'] in final:
								# print('boolean found***????????????????',val['key'],final)
								pos = 0
								# print("val is",n_val)
								for idx,word in enumerate(final.split()):
									if val['key'].lower() in word:
										pos = idx
										if "flex" in word:
											if "no "+word in final:
												# for iob final = re.sub("no "+word,'$'+val['key']+'$', final, 1)
												# final = final.replace("no "+word,'$'+val['key']+'$')
												print("herereeeeeeeeeeeeeeeeeeeeeeeeee")
												tag = "B_"+val['key']
												iob[pos-1] = iob[pos-1].replace("O", tag)
												tag = "I_"+val['key']
												iob[pos] = iob[pos].replace("O", tag)
												if args['name'] not in ontology:
													ontology[args['name']] = {}
												if val['key'] not in ontology[args['name']]:
													ontology[args['name']][val['key']] = {}
												for onto_iter in range(len(ontology[args['name']][val['key']]),len(ontology[args['name']][val['key']])+1):
													if "no "+word not in ontology[args['name']][val['key']].values():
														print("not in")	
														ontology[args['name']][val['key']][onto_iter] = "no "+word
												# onto_key = onto_key+1
												print("no '''''")
											elif "no"+word in final:
												# for iob final = re.sub("no"+word,'$'+val['key']+'$', final, 1)
												# final = final.replace("no"+word,'$'+val['key']+'$')
												tag = "B_"+val['key']
												iob[pos] = iob[pos].replace("O", tag)
												if args['name'] not in ontology:
													ontology[args['name']] = {}
												if val['key'] not in ontology[args['name']]:
													ontology[args['name']][val['key']] = {}
												for onto_iter in range(len(ontology[args['name']][val['key']]),len(ontology[args['name']][val['key']])+1):
													if "no"+word not in ontology[args['name']][val['key']].values():
														ontology[args['name']][val['key']][onto_iter] = "no"+word
												# onto_key = onto_key+1
											elif "not"+word in final:
												# final = final.replace("not"+word,'$'+val['key']+'$')
												# for iob final = re.sub("not"+word,'$'+val['key']+'$', final, 1)
												tag = "B_"+val['key']
												iob[pos] = iob[pos].replace("O", tag)
												if args['name'] not in ontology:
													ontology[args['name']] = {}
												if val['key'] not in ontology[args['name']]:
													ontology[args['name']][val['key']] = {}
												for onto_iter in range(len(ontology[args['name']][val['key']]),len(ontology[args['name']][val['key']])+1):
													if "not"+word not in ontology[args['name']][val['key']]:
														ontology[args['name']][val['key']][onto_iter] = "not"+word
												# onto_key = onto_key+1
											elif "not "+word in final:
												# final = final.replace("not "+word,'$'+val['key']+'$')
												# for iob final = re.sub("not "+word,'$'+val['key']+'$', final, 1)
												tag = "B_"+val['key']
												iob[pos-1] = iob[pos-1].replace("O", tag)
												tag = "I_"+val['key']
												iob[pos] = iob[pos].replace("O", tag)
												if args['name'] not in ontology:
													ontology[args['name']] = {}
												if val['key'] not in ontology[args['name']]:
													ontology[args['name']][val['key']] = {}
												for onto_iter in range(len(ontology[args['name']][val['key']]),len(ontology[args['name']][val['key']])+1):
													if "not "+word not in ontology[args['name']][val['key']].values():
														ontology[args['name']][val['key']][onto_iter] = "not "+word
												# onto_key = onto_key+1
											else:								
												# final = final.replace(word,'$'+val['key']+'$')
												# for iob final = re.sub(word,'$'+val['key']+'$', final, 1)
												tag = "B_"+val['key']
												iob[pos] = iob[pos].replace("O", tag)
												if args['name'] not in ontology:
													ontology[args['name']] = {}
												if val['key'] not in ontology[args['name']]:
													ontology[args['name']][val['key']] = {}
												for onto_iter in range(len(ontology[args['name']][val['key']]),len(ontology[args['name']][val['key']])+1):
													if word not in ontology[args['name']][val['key']].values():	
														ontology[args['name']][val['key']][onto_iter] = word
												# onto_key = onto_key+1
										# elif "wifi" in word:
										# 	if "free "+word in final:
										# 		final = final.replace("free "+word,'$'+val['key']+'$')
										# 		print("no '''''")
										# 	elif "free"+word in final:
										# 		final = final.replace("free"+word,'$'+val['key']+'$')
										# 	else:								
										# 		final = final.replace(word,'$'+val['key']+'$')
										else:
											if "free "+word in final:
												# final = final.replace("free "+word,'$'+val['key']+'$')
												# for iob final = re.sub("free "+word,'$'+val['key']+'$', final, 1)
												tag = "B_"+val['key']
												iob[pos-1] = iob[pos-1].replace("O", tag)
												print("tag",tag,iob,pos)
												tag = "I_"+val['key']
												iob[pos] = iob[pos].replace("O", tag)
												print("final",final)
												print("tag2",tag,iob)
												if args['name'] not in ontology:
													ontology[args['name']] = {}
												if val['key'] not in ontology[args['name']]:
													ontology[args['name']][val['key']] = {}
												for onto_iter in range(len(ontology[args['name']][val['key']]),len(ontology[args['name']][val['key']])+1):
													if "free "+word not in ontology[args['name']][val['key']].values():
														ontology[args['name']][val['key']][onto_iter] = "free "+word
												# onto_key = onto_key+1
												print("no '''''")
											elif "free"+word in final:
												tag = "B_"+val['key']
												iob[pos] = iob[pos].replace("O", tag)
												# final = final.replace("free"+word,'$'+val['key']+'$')
												# for iob final = re.sub("free"+word,'$'+val['key']+'$', final, 1)
												if args['name'] not in ontology:
													ontology[args['name']] = {}
												if val['key'] not in ontology[args['name']]:
													ontology[args['name']][val['key']] = {}
												for onto_iter in range(len(ontology[args['name']][val['key']]),len(ontology[args['name']][val['key']])+1):
													if "free"+word not in ontology[args['name']][val['key']].values():
														ontology[args['name']][val['key']][onto_iter] = "free"+word
												# onto_key = onto_key+1
											else:	
												tag = "B_"+val['key']
												iob[pos] = iob[pos].replace("O", tag)							
												# final = final.replace(word,'$'+val['key']+'$')
												# for iob final = re.sub(word,'$'+val['key']+'$', final, 1)
												if args['name'] not in ontology:
													ontology[args['name']] = {}
												if val['key'] not in ontology[args['name']]:
													ontology[args['name']][val['key']] = {}
												for onto_iter in range(len(ontology[args['name']][val['key']]),len(ontology[args['name']][val['key']])+1):
													if word not in ontology[args['name']][val['key']].values():
														ontology[args['name']][val['key']][onto_iter] = word
												# onto_key = onto_key+1
										# else:			
										# 	final = final.replace(word,'$'+val['key']+'$')
										slots.append(val['key'])

										act.append(args['name'])
										# if args['name'] not in ontology:
										# 	ontology[args['name']] = {}
										# if val['key'] not in ontology[args['name']]:
										# 	ontology[args['name']][val['key']] = {}
										# ontology[args['name']][val['key']][onto_key] = n_val
										# onto_key = onto_key+1
										boolean.append(val['key']) #get boolean keys
										text.append(final)
										print("position brek",pos)
										break
								# tag = "B_"+val['key']
								# iob[pos] = iob[pos].replace("O", tag)
								# if val['key'] in final:
								# 	tag = "B_"+val['key']
								# 	iob[pos] = iob[pos].replace("O", tag)
								# 	print("----------------------------")
								# 	print(iob)
								# 	print(final)
								# 	print("----------------------------")

								wc = 0
							# wc = len(n_val.split())
							if wc == 1:
								pos = 0
								print("val is",n_val)
								for idx,word in enumerate(final.split()):
									if n_val in word:
										pos = idx
										print("position brek",pos)
										# for iob final = re.sub(n_val,'$'+val['key']+'$', final, 1)
										# final = final.replace(word,'$'+val['key']+'$')
										slots.append(val['key'])
										act.append(args['name'])
										if args['name'] not in ontology:
											ontology[args['name']] = {}
										if val['key'] not in ontology[args['name']]:
											ontology[args['name']][val['key']] = {}
										for onto_iter in range(len(ontology[args['name']][val['key']]),len(ontology[args['name']][val['key']])+1):
											if n_val not in ontology[args['name']][val['key']].values():
												ontology[args['name']][val['key']][onto_iter] = n_val
										# onto_key = onto_key+1
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
											print(word,idx,idy)

											pos = idy
											# print("position brek",pos)
											if idx == 0:
												tag = "B_"+val['key']
												if iob[pos] == " O" or iob[pos] == "O":
													print("==0")
													iob[pos] = iob[pos].replace("O", tag)
												else:
													continue
												# break
											else:
												tag = "I_"+val['key']
												if iob[pos] == " O" or iob[pos] == "O" :
													print("===0")
													iob[pos] = iob[pos].replace("O", tag)
												else:
													continue
												# break
											break
								# for word in range(len)
								# final = final.replace(n_val,'$'+val['key']+'$')
								# for iob final = re.sub(n_val,'$'+val['key']+'$', final, 1)
								slots.append(val['key'])
								act.append(args['name'])
								if args['name'] not in ontology:
									ontology[args['name']] = {}
								if val['key'] not in ontology[args['name']]:
									ontology[args['name']][val['key']] = {}
								for onto_iter in range(len(ontology[args['name']][val['key']]),len(ontology[args['name']][val['key']])+1):
									if n_val not in ontology[args['name']][val['key']].values():
										ontology[args['name']][val['key']][onto_iter] = n_val
								# onto_key = onto_key+1

							else:
								print("0 words")
							temp =temp+1
					f.write(intent)
					f.write('\n')
					# f.write(''.join(slots))
					# f.write('\n')
					# final="BOS "+final+" EOS"
					f.write(final +"\n") 
					# iob = ["O "]+ iob
					# iob.append(" O")
					f.write(''.join(iob))
					f.write('\n')	
					for k in range(len(act), 4):
						act.append('xxx')
					for l in range(len(slots), 4):
						slots.append('xxx')
					print("- - - - - - - - - - - - - - - - - - - - -- - - - - -")
					print(final,act,slots)
					if 'xxx' not in act[0]:
						df.loc[num] = pd.Series(dict(nl=final, act1=act[0], act2=act[1], act3=act[2], act4=act[3], slot1= slots[0], slot2= slots[1], slot3= slots[2], slot4= slots[3]))
						num=num+1
					# jk = [[final,act[0],act[1],act[2],act[3],slots[0],slots[1],slots[2],slots[3]]]
					# kj.append(final,act[0],act[1],act[2],act[3],slots[0],slots[1],slots[2],slots[3])
					# kj.append(jk)
					# print(kj)
					# df.append({'nl': final, 'act1':act[0], 'act2':act[1], 'act3':act[2], 'slot1':slots[0], 'slot2':slots[1], 'slot3':slots[2]}, ignore_index=True)
					# crf.append(list(zip(final,act[0],act[1],act[2],act[3],slots[0],slots[1],slots[2],slots[3])))
					# print(crf)
					# df = pd.DataFrame(jk, columns=['nl','act1','act2','act3','act4','slot1','slot2','slot3','slot4'])
					
				
					# for act in item['labels']['frames']:
					# 	if 'intent' in act['info']:
					# 		for intent in act['info']['intent']:
					# 			print(intent['val'])
					# print(df)
		df.to_csv('iob crf_new2.csv', index=False)     
		print("boolean",boolean ,text)
		# with open('unused_acts', 'w') as outfile: #by jose
		# 	json.dump(set(no_slots),outfile)
		with open('iob ontology2.json', 'w') as outfile: #by jose
			json.dump(ontology, outfile)
		# f.write(''.join(set(no_slots)))	
