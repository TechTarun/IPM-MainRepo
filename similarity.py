# from gensim.models.word2vec import Word2Vec
# import gensim.downloader as api
# # import base 

# # model = api.load('glove-twitter-25')
# model = api.load('glove-wiki-gigaword-100')
# # model = models.KeyedVectors.load_word2vec_format('./model.bin', binary=True)
# # model = Word2Vec(corpus)

# while(True):
#     word1 = input("Enter first word = ")

#     # print(model.most_similar(word1))
#     query_type_list =['create', 'delete', 'update', 'details', 'transition', 'assign']

#     for word2 in query_type_list:
#         print(word2, "->", model.similarity(word1, word2))


# #0.76, 0.70, 0.92,  

def printArgs(**args):
    print(args["name"])
    print(args["user"])


args = {"name" : "xyz", "user" : "abc"}
printArgs(**args)