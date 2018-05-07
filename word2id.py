import json
import re
# with open('nlg_train_temp.txt', 'w') as f:
utterances = list()
tags = list()
starts = list()
startid = list()

# reserving index 0 for padding
# reserving index 1 for unknown word and tokens
word_vocab_index = 4
tag_vocab_index = 4
word2id = {'<s>':0, '<pad>':1, '</s>':2, '<unk>':3}
tag2id = {'<s>':0, '<pad>':1, '</s>':2, '<unk>':3}
id2word = ['<s>','<pad>','</s>','<unk>']
id2tag = ['<s>','<pad>','</s>','<unk>']
src_data={}
trg_data={}
utt_count = 0
temp_startid = 0
count=0
for line in open('nlg_train_temp.txt', 'r'):
	d=line.split('\t')
	print("checking datafile  ",line)
	print("checking datafile2  ",d)
	intents = d[0].strip()
	# print("checking datafile  ",utt)
	words = d[1].strip()
	# print("checking datafile  ",t)
	# if len(d) > 2:
	# 	start = np.bool(int(d[2].strip()))
	# 	starts.append(start)
	# 	if start:
	# 		temp_startid = utt_count
	# 	startid.append(temp_startid)
	#print 'utt: %s, tags: %s' % (utt,t) 

	temp_intents = list()
	temp_words = list()
	mywords = words.split()
	mytags = intents.split()
	src_data[count]=mywords
	trg_data[count]=mytags
	count=count+1
	# if len(mywords) != len(mytags):
	# 	print mywords
	# 	print mytags
	# now add the words and tags to word and tag dictionaries
	# also save the word and tag sequence in training data sets
	for i in range(len(mywords)):
		if mywords[i] not in word2id:
			word2id[mywords[i]] = word_vocab_index
			id2word.append(mywords[i])
			word_vocab_index += 1
		temp_words.append(word2id[mywords[i]])
	for j in range(len(mytags)):
		if mytags[j] not in tag2id:
			tag2id[mytags[j]] = tag_vocab_index
			id2tag.append(mytags[j])
			tag_vocab_index += 1
		temp_intents.append(tag2id[mytags[j]])
	utt_count += 1
	utterances.append(temp_words)
	tags.append(temp_intents)

	with open('src_word2id.json', 'w') as outfile:
	    json.dump(word2id, outfile)
	    
	with open('src_id2word.json','w') as outfile:
		json.dump(id2word, outfile)
	with open('trg_tag2id.json', 'w') as outfile:
	    json.dump(tag2id, outfile)
	with open('trg_id2tag.json','w') as outfile:
	    json.dump(id2tag, outfile)
	with open('src_data.json', 'w') as outfile:
	    json.dump(src_data, outfile)

	with open('trg_data.json', 'w') as outfile:
	    json.dump(trg_data, outfile)



# data = {'start': starts, 'startid': startid, 'utterances': utterances, 'tags': tags, 'uttCount': utt_count, 'id2word':id2word, 'id2tag':id2tag, 'wordVocabSize' : word_vocab_index, 'tagVocabSize': tag_vocab_index, 'word2id': word2id, 'tag2id':tag2id}
# return data
