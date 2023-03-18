# To determine whether two texts are written about the same subject using natural language processing (NLP) techniques, you can use a text similarity model. This type of model takes two texts as input and outputs a score indicating how similar the texts are in terms of their subject matter.

# Here is an example of how you might use a pre-trained text similarity model, such as BERT, to check whether two texts are written about the same subject:

# Copy code
import transformers


# Load the BERT model

# model = transformers.BertModel.from_pretrained("bert-base-uncased")
#
# # Define the two texts to compare
# text1 = "The world is a beautiful place full of amazing sights and experiences."
# text2 = "There are many wonders to be found in nature, from the tallest mountains to the deepest oceans."
# tokenizer = transformers.BatchEncoding  # TODO: need to verify this
# # Encode the texts as input for the BERT model
# inputs = tokenizer.encode_plus(text1, text2, return_tensors="pt", max_length=128)
#
# # Pass the encoded inputs through the BERT model
# outputs = model(**inputs)
#
# # Calculate the similarity score between the texts
# similarity_score = outputs[0][0][0].item()
#
# # Print the similarity score
# print(f"Similarity score: {similarity_score}")
#

# This code uses the Hugging Face transformers library to load a pre-trained BERT model and calculate the similarity score between the two input texts. The score will be a value between 0 and 1, with higher values indicating that the texts are more similar in terms of their subject matter.

# You can adjust the parameters of the BERT model and the similarity calculation to fine-tune the results to your specific needs. Additionally, you may want to use other NLP techniques, such as keyword extraction or text summarization, to further analyze the texts and determine their similarity.

class Bert:
    def __init__(self, tokenizer=transformers.BatchEncoding()):
        self.tokenizer = tokenizer
        self.model = transformers.BertModel.from_pretrained("bert-base-uncased")


    def similarity(self, text1, text2, maxlen):
        inputs = self.tokenizer.encode_plus(text1, text2, return_tensors="pt", max_length=maxlen)
        outputs = self.model(**inputs)
        similarity_score = outputs[0][0][0].item()
        return similarity_score
