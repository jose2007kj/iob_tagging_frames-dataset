#modified on 8-3-2018
#added code for testing joint slu

import json
# import nltk
# nltk.download('punkt')
# from nltk.tokenize import wordpunct_tokenize
import re
# import numpy as np
# import pandas as pd
# from pandas import DataFrame, read_csv
with open('trash.iob', 'w') as f:
	with open('frames.json', 'r') as file_object:
		contents = json.load(file_object)
		crf = []
		kj = []
		num = 0
		no_slots = []
		ontology = {}
		travel_dict = {}
		onto_key = 0
		boolean = []
		text = []
		travel_key = 0
		# df=pd.DataFrame(columns=['nl', 'act1', 'act2', 'act3', 'act4', 'slot1', 'slot2', 'slot3', 'slot4'])
		for i in range(0,1350):
			print(i, '****************************')
			for item in contents[i]['turns']:
				if 'user' in item['author']:
					if travel_key not in travel_dict:
						travel_dict[travel_key] = {'palace':'','seat':'','duration':'','str_date':'','cathedral':'','gst_rating':'','spa':'','category':''
,'museum':''
,'or_city':''
,'beach':''
,'end_date':''
,'ref_anaphora':''
,'price':''
,'park':''
,'downtown':''
,'dst_city':''
,'n_adults':''
,'name':''
,'university':''
,'dep_time_or':''
,'airport':''
,'amenities':''
,'wifi':''
,'budget':''
,'parking':''
,'breakfast':''
,'count_name':''
,'count':''
,'n_children':''
,'count_dst_city':''
,'count_seat':''
,'flex':''
,'vicinity':''
,'dep_time_dst':''
,'gym':''
,'shopping':''
,'mall':''
,'max_duration':''
,'market':''
,'arr_time_or':''
,'min_duration':''
,'thankyou':''
,'goodbye':''
,'affirm':''
,'greeting':''
,'negate':''}
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
									# n_val = n_val.replace('$', '')
									n_val = re.sub(r"\.+", " ", n_val)
									n_val = re.sub(r"\?+", " ", n_val)# remove ?
									n_val = re.sub(r"\!+", " ", n_val)#remove !
									n_val =n_val.rstrip()
									pattern = re.compile(r'\s+')
									n_val = re.sub(pattern," ", n_val)
									n_val= n_val.replace('$',"") #for removing $
									# print("+++++++++++++++++++++",n_val,final)
									# n_val = val['val']
									n_val = n_val.lower()
									# print("val",n_val)
									wc = len(n_val.split())
									# slot[temp] = val['key']
							else:
								# print("else val,key",val['val'],val['key'])
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
												# print("herereeeeeeeeeeeeeeeeeeeeeeeeee")
												tag = "B_"+args['name']+"_"+val['key']
												iob[pos-1] = iob[pos-1].replace("O", tag)
												tag = "I_"+args['name']+"_"+val['key']
												iob[pos] = iob[pos].replace("O", tag)
												# if val[key] not in ontology:
												# 	ontology[args['name']] = {}
												travel_temp={val['key']:'no flexible'}
												travel_dict[travel_key].update(travel_temp)
												# travel_dict[travel_key][val['key']]= 'no flexible'
												#travel_key =travel_key+1
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
												tag = "B_"+args['name']+"_"+val['key']
												iob[pos] = iob[pos].replace("O", tag)
												if args['name'] not in ontology:
													ontology[args['name']] = {}
												if val['key'] not in ontology[args['name']]:
													ontology[args['name']][val['key']] = {}
												for onto_iter in range(len(ontology[args['name']][val['key']]),len(ontology[args['name']][val['key']])+1):
													if "no"+word not in ontology[args['name']][val['key']].values():
														ontology[args['name']][val['key']][onto_iter] = "no"+word
												# travel_dict[travel_key][val['key']]= 'noflexible'
												travel_temp={val['key']:'noflexible'}
												# travel_dict
												travel_dict[travel_key].update(travel_temp)
												#travel_key =travel_key+1
												# onto_key = onto_key+1
											elif "not"+word in final:
												# final = final.replace("not"+word,'$'+val['key']+'$')
												# for iob final = re.sub("not"+word,'$'+val['key']+'$', final, 1)
												tag = "B_"+args['name']+"_"+val['key']
												iob[pos] = iob[pos].replace("O", tag)
												if args['name'] not in ontology:
													ontology[args['name']] = {}
												if val['key'] not in ontology[args['name']]:
													ontology[args['name']][val['key']] = {}
												for onto_iter in range(len(ontology[args['name']][val['key']]),len(ontology[args['name']][val['key']])+1):
													if "not"+word not in ontology[args['name']][val['key']]:
														ontology[args['name']][val['key']][onto_iter] = "not"+word
												# travel_dict[travel_key][val['key']]= 'notflexible'
												travel_temp={val['key']:'notflexible'}
												travel_dict[travel_key].update(travel_temp)
												#travel_key =travel_key+1
												# onto_key = onto_key+1
											elif "not "+word in final:
												# final = final.replace("not "+word,'$'+val['key']+'$')
												# for iob final = re.sub("not "+word,'$'+val['key']+'$', final, 1)
												tag = "B_"+args['name']+"_"+val['key']
												iob[pos-1] = iob[pos-1].replace("O", tag)
												tag = "I_"+args['name']+"_"+val['key']
												iob[pos] = iob[pos].replace("O", tag)
												if args['name'] not in ontology:
													ontology[args['name']] = {}
												if val['key'] not in ontology[args['name']]:
													ontology[args['name']][val['key']] = {}
												for onto_iter in range(len(ontology[args['name']][val['key']]),len(ontology[args['name']][val['key']])+1):
													if "not "+word not in ontology[args['name']][val['key']].values():
														ontology[args['name']][val['key']][onto_iter] = "not "+word
												# travel_dict[travel_key][val['key']]= 'not flexible'
												travel_temp={val['key']:'not flexible'}
												travel_dict[travel_key].update(travel_temp)
												#travel_key =travel_key+1
												# onto_key = onto_key+1
											else:								
												# final = final.replace(word,'$'+val['key']+'$')
												# for iob final = re.sub(word,'$'+val['key']+'$', final, 1)
												tag = "B_"+args['name']+"_"+val['key']
												iob[pos] = iob[pos].replace("O", tag)
												if args['name'] not in ontology:
													ontology[args['name']] = {}
												if val['key'] not in ontology[args['name']]:
													ontology[args['name']][val['key']] = {}
												for onto_iter in range(len(ontology[args['name']][val['key']]),len(ontology[args['name']][val['key']])+1):
													if word not in ontology[args['name']][val['key']].values():	
														ontology[args['name']][val['key']][onto_iter] = word
												# travel_dict[travel_key][val['key']]= 'flexible'
												travel_temp={val['key']:'flexible'}
												travel_dict[travel_key].update(travel_temp)
												#travel_key =travel_key+1
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
												tag = "B_"+args['name']+"_"+val['key']
												iob[pos-1] = iob[pos-1].replace("O", tag)
												# print("tag",tag,iob,pos)
												tag = "I_"+args['name']+"_"+val['key']
												iob[pos] = iob[pos].replace("O", tag)
												# print("final",final)
												# print("tag2",tag,iob)
												if args['name'] not in ontology:
													ontology[args['name']] = {}
												if val['key'] not in ontology[args['name']]:
													ontology[args['name']][val['key']] = {}
												for onto_iter in range(len(ontology[args['name']][val['key']]),len(ontology[args['name']][val['key']])+1):
													if "free "+word not in ontology[args['name']][val['key']].values():
														ontology[args['name']][val['key']][onto_iter] = "free "+word
												# travel_dict[travel_key][val['key']]= 'free '+word
												travel_temp={val['key']:'free '+word}
												travel_dict[travel_key].update(travel_temp)
												#travel_key =travel_key+1
												# onto_key = onto_key+1
												print("no '''''")
											elif "free"+word in final:
												tag = "B_"+args['name']+"_"+val['key']
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
												# travel_dict[travel_key][val['key']]= 'free'+word
												travel_temp={val['key']:'free'+word}
												travel_dict[travel_key].update(travel_temp)
												#travel_key =travel_key+1
												# onto_key = onto_key+1
											else:	
												tag = "B_"+args['name']+"_"+val['key']
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
												# travel_dict[travel_key][val['key']]= word
												travel_temp={val['key']:word}
												travel_dict[travel_key].update(travel_temp)
												#travel_key =travel_key+1
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
										# print("position brek",pos)
										break
								# tag = "B_"+args['name']+"_"+val['key']
								# iob[pos] = iob[pos].replace("O", tag)
								# if val['key'] in final:
								# 	tag = "B_"+args['name']+"_"+val['key']
								# 	iob[pos] = iob[pos].replace("O", tag)
								# 	print("----------------------------")
								# 	print(iob)
								# 	print(final)
								# 	print("----------------------------")

								wc = 0
							# wc = len(n_val.split())
							if wc == 1:
								pos = 0
								# print("val is",n_val)
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
								# print(final)
								# print("1 word match? ",n_val, pos)
								# res = int(indices)
								# indices = int(indices)
								# print(res)
								tag = "B_"+args['name']+"_"+val['key']
								iob[pos] = iob[pos].replace("O", tag)
								# travel_dict[travel_key][val['key']]= n_val
								travel_temp={val['key']:n_val}
								travel_dict[travel_key].update(travel_temp)
								#travel_key =travel_key+1
								# for x in range(0,len(iob)): #working for loop
								# 	iob[x] = iob[x].replace("O", "nmnmnm")
								# 	print("iob",iob[x])
							elif wc > 1:
								# print("more than 1 word",wc)
								# print("testing---------------------------",n_val)
								for idx,word in enumerate(n_val.split()):
									for idy,word2 in enumerate(final.split()):

										if word in word2:
											print(word,idx,idy)
											# travel_dict[travel_key][val['key']]= n_val
											travel_temp={val['key']:n_val}
											travel_dict[travel_key].update(travel_temp)
											#travel_key =travel_key+1
											pos = idy
											# print("position brek",pos)
											if idx == 0:
												tag = "B_"+args['name']+"_"+val['key']
												if iob[pos] == " O" or iob[pos] == "O":
													print("testing---------------------------",n_val)
													print("testing%skj"%iob[pos])
													print("==0")
													iob[pos] = iob[pos].replace("O", tag)
													print("testing---------------------------",n_val,iob[pos])
												else:
													continue
												# break
											else:
												tag = "I_"+args['name']+"_"+val['key']
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
					# f.write(intent)
					# f.write('\n')
					# f.write(''.join(slots))
					# f.write('\n')
					final="BOS "+final+" EOS"
					f.write(final)
					f.write("\t") 
					# f.write(''.join(iob))

					# f.write(" "+intent+"\n")
					iob = ["O "]+ iob
					iob.append(" O")
					# f.write(''.join(iob))
					# f.write("\t")
					# f.write(intent)
					# f.write("\n")
					# f.write('\n')
					iob_count = 0	
					for word in iob:
						if word == " O" or word == "O" or word == "O ":
							iob_count = iob_count +1
						# if "B_"+args['name']+"_" not in word:
						# 	print("8888888888888888888888",word)
						# elif "I_"+args['name']+"_" not in word:
						# 	print("8888888888888888888888",word)
					print("**************************",iob,len(iob),iob_count)
					ll = 0
					greeting = ['hi','hello','heyo','hey','greetings']
					moreinfo = ['more','details']
					affirm = ['ok','ya','yeah','please do','yes']
					# thankyou= = ['thank]
					if len(iob) == iob_count:
						print("^^^^^^^^#########################################################^^^^^^^^^^",iob,intent)
						intentlist = intent.split()
						# intentlist= [i for i in words if i.lower() not in stopwords]
						for i, w in enumerate(intentlist):
							if w == 'confirm':
								intentlist[i] ='affirm'
								print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

						ioblen = len(iob)
						# for k in range(0,len(intentlist)): #working code for inserting intenbt
							# if k ==0:
							# 	iob[k+1]=intentlist[k]
							# else:
							# 	iob[k+1]= " "+intentlist[k]  #end here
						for l,m in enumerate(final.split()):
							if l == 1:
								if m == 'good':
									if final[l+1] == 'afternoon' or final[l+1] == 'evening' or final[l+1] == 'morning':
										# if k == 0:
										iob[l]="B_greeting"
										iob[l+1]=" I_greeting"
										# travel_dict[travel_key]['greeting']= 'good '+final[l+1]
										travel_temp={'greeting':'good '+final[l+1]}
										travel_dict[travel_key].update(travel_temp)
										#travel_key =travel_key+1
								elif m in greeting:
									iob[l] = "B_greeting"
									# travel_dict[travel_key]['greeting']= m
									travel_temp={'greeting':m}
									travel_dict[travel_key].update(travel_temp)
									#travel_key =travel_key+1
								elif m in moreinfo:
									# travel_dict[travel_key]['moreinfo']= m
									travel_temp={'moreinfo':m}
									travel_dict[travel_key].update(travel_temp)
									#travel_key =travel_key+1
									iob[l] = 'B_moreinfo'
								elif m in affirm:
									# travel_dict[travel_key]['affirm']= m
									travel_temp={'affirm':m}
									travel_dict[travel_key].update(travel_temp)
									#travel_key =travel_key+1
									iob[l] = 'B_affirm'
								elif "thank" in m:
									# travel_dict[travel_key]['thankyou']= m
									travel_temp={'thankyou':m}
									travel_dict[travel_key].update(travel_temp)
									#travel_key =travel_key+1
									iob[l] = "B_thankyou"
								elif 'bye' in m:
									# travel_dict[travel_key]['goodbyye']= m
									travel_temp={'goodbye':m}
									travel_dict[travel_key].update(travel_temp)
									#travel_key =travel_key+1
									iob[l] = 'B_goodbye'
								elif 'no' == m or 'nope' == m:
									# travel_dict[travel_key]['negate']= m
									travel_temp={'negate':m}
									travel_dict[travel_key].update(travel_temp)
									#travel_key =travel_key+1
									iob[l] = 'B_negate'
								else:
									print("b")
							else:
								if m == 'good':
									if final[l+1] == 'afternoon' or final[l+1] == 'evening' or final[l+1] == 'morning':
										# if k == 0:
										iob[l]=" B_greeting"
										iob[l+1]=" I_greeting"
										travel_temp={'greeting':'good '+final[l+1]}
										travel_dict[travel_key].update(travel_temp)
										#travel_key =travel_key+1
								elif m in greeting:
									iob[l] = " B_greeting"
									travel_temp={'greeting':m}
									travel_dict[travel_key].update(travel_temp)
									#travel_key =travel_key+1
								elif m in moreinfo:
									iob[l] = ' B_moreinfo'
									travel_temp={'moreinfo':m}
									travel_dict[travel_key].update(travel_temp)
									#travel_key =travel_key+1
								elif m in affirm:
									iob[l] = ' B_affirm'
									travel_temp={'affirm':m}
									travel_dict[travel_key].update(travel_temp)
									#travel_key =travel_key+1
								elif "thank" in m:
									iob[l] = " B_thankyou"
									travel_temp={'thankyou':m}
									travel_dict[travel_key].update(travel_temp)
									#travel_key =travel_key+1
								elif 'bye' in m:
									iob[l] = ' B_goodbye'
									travel_temp={'goodbye':m}
									travel_dict[travel_key].update(travel_temp)
									#travel_key =travel_key+1
								elif 'no' == m or 'nope' == m:
									travel_temp={'negate':m}
									travel_dict[travel_key].update(travel_temp)
									#travel_key =travel_key+1
									iob[l] = ' B_negate'
								else:
									print("b")



								# if m in greeting:

							
							# if intentlist[k] == 'greeting':


						
					f.write(''.join(iob))
					f.write("\n")
					# f.write(intent)
					# f.write("\n")
						# print("@@@@@@@@@@@@@@@@",iob)
					for k in range(len(act), 4):
						act.append('xxx')
					for l in range(len(slots), 4):
						slots.append('xxx')
					print("- - - - - - - - - - - - - - - - - - - - -- - - - - -")
					print(final,act,slots)
					if 'xxx' not in act[0]:
						# df.loc[num] = pd.Series(dict(nl=final, act1=act[0], act2=act[1], act3=act[2], act4=act[3], slot1= slots[0], slot2= slots[1], slot3= slots[2], slot4= slots[3]))
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
			travel_key =travel_key+1

		# df.to_csv('iob crf_new2.csv', index=False)     
		# print("boolean",boolean ,text)
		# with open('unused_acts', 'w') as outfile: #by jose
		# 	json.dump(set(no_slots),outfile)
		# with open('iob ontology2.json', 'w') as outfile: #by jose
		# 	json.dump(ontology, outfile)
		# f.write(''.join(set(no_slots)))	

		# 			ll = 0
		# 			greeting = ['hi','hello','heyo','good morning','hey','greetings']
		# 			moreinfo = ['more','details']
		# 			affirm = ['ok','ya','yeah','please do','yes']
		# 			if len(iob) == iob_count:
		# 				print("^^^^^^^^#########################################################^^^^^^^^^^",iob,intent)
		# 				intentlist = intent.split()
		# 				# intentlist= [i for i in words if i.lower() not in stopwords]
		# 				for i, w in enumerate(intentlist):
		# 					if w == 'confirm'
		# 						intentlist[i] ='affirm'

		# 				ioblen = len(iob)
		# 				for k in range(0,len(intentlist)): #working code for inserting intenbt
		# 					if k ==0:
		# 						iob[k+1]=intentlist[k]
		# 					else:
		# 						iob[k+1]= " "+intentlist[k]  #end here
		# 					if intentlist[k] == 'greeting':


						
		# 			f.write(''.join(iob))
		# 			f.write("\n")
		# 			# f.write(intent)
		# 			# f.write("\n")
		# 				# print("@@@@@@@@@@@@@@@@",iob)
		# 			for k in range(len(act), 4):
		# 				act.append('xxx')
		# 			for l in range(len(slots), 4):
		# 				slots.append('xxx')
		# 			print("- - - - - - - - - - - - - - - - - - - - -- - - - - -")
		# 			print(final,act,slots)
		# 			if 'xxx' not in act[0]:
		# 				# df.loc[num] = pd.Series(dict(nl=final, act1=act[0], act2=act[1], act3=act[2], act4=act[3], slot1= slots[0], slot2= slots[1], slot3= slots[2], slot4= slots[3]))
		# 				num=num+1
		# 			# jk = [[final,act[0],act[1],act[2],act[3],slots[0],slots[1],slots[2],slots[3]]]
		# 			# kj.append(final,act[0],act[1],act[2],act[3],slots[0],slots[1],slots[2],slots[3])
		# 			# kj.append(jk)
		# 			# print(kj)
		# 			# df.append({'nl': final, 'act1':act[0], 'act2':act[1], 'act3':act[2], 'slot1':slots[0], 'slot2':slots[1], 'slot3':slots[2]}, ignore_index=True)
		# 			# crf.append(list(zip(final,act[0],act[1],act[2],act[3],slots[0],slots[1],slots[2],slots[3])))
		# 			# print(crf)
		# 			# df = pd.DataFrame(jk, columns=['nl','act1','act2','act3','act4','slot1','slot2','slot3','slot4'])
					
				
		# 			# for act in item['labels']['frames']:
		# 			# 	if 'intent' in act['info']:
		# 			# 		for intent in act['info']['intent']:
		# 			# 			print(intent['val'])
		# 			# print(df)
		# # df.to_csv('iob crf_new2.csv', index=False)     
		# # print("boolean",boolean ,text)
		# # with open('unused_acts', 'w') as outfile: #by jose
		# # 	json.dump(set(no_slots),outfile)
		with open('travel_dict.json', 'w') as outfile: #by jose
			json.dump(travel_dict, outfile)
		# # f.write(''.join(set(no_slots)))	
