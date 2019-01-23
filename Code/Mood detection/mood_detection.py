# You need to check you have pytorch 1.0.0 and pip install flair
from flair.embeddings import WordEmbeddings
from flair.data import Sentence


# Choose embedding
embedding_method_list = ['glove','extvec','crawl','twitter','news']
embedding_method = 'glove'

embedding = WordEmbeddings(embedding_method)




# create sentence.
sentence = Sentence('The grass is green .')
# here sentence will be our lyrics, one song is an epoch

# embed a sentence using glove.
embedding.embed(sentence)


# now check out the embedded tokens.
for token in sentence:
    print(token)
    print(token.embedding)

