import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sentence_transformers import SentenceTransformer, util
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoModel, AutoTokenizer
from logger import log_function
from transformers import pipeline, AutoTokenizer


# def try_transformers(text1,text2):
#     model = SentenceTransformer('stsb-roberta-large')
#     embedding1 = model.encode(text1, convert_to_tensor=True)
#     embedding2 = model.encode(text2, convert_to_tensor=True)
#     cosine_scores = util.pytorch_cos_sim(embedding1, embedding2)
#     return cosine_scores.item()

def preprocess_text(text):
    # Tokenize the text
    tokens = word_tokenize(text.lower())

    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    filtered_tokens = [token for token in tokens if token not in stop_words]

    # Lemmatize the tokens
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]

    # Join the tokens back into a single string
    preprocessed_text = " ".join(lemmatized_tokens)

    return preprocessed_text


# model = 'projecte-aina/roberta-base-ca-cased-sts'
# #model = AutoModel.from_pretrained(model)
# tokenizer = AutoTokenizer.from_pretrained(model)
# pipe = pipeline('text-classification', model=model, tokenizer=tokenizer)
#
#
# def prepare(sentence_pairs):
#     sentence_pairs_prep = []
#     for s1, s2 in sentence_pairs:
#         sentence_pairs_prep.append(
#             f"{tokenizer.cls_token} {s1}{tokenizer.sep_token}{tokenizer.sep_token} {s2}{tokenizer.sep_token}")
#     return sentence_pairs_prep
#
#
# def rob_sim(text1, text2):
#     from scipy.special import logit
#
#     # sentence_pairs = [("El llibre va caure per la finestra.", "El llibre va sortir volant."),
#     #                  ("M'agrades.", "T'estimo."),
#     #                  ("M'agrada el sol i la calor", "A la Garrotxa plou molt.")]
#
#     predictions = pipe(prepare([(text1, text2)]), add_special_tokens=False)
#     return logit(predictions[0]['score'])
#     # convert back to scores to the original 0 and 5 interval
#     # for prediction in predictions:
#     #    prediction['score'] = logit(prediction['score'])


@log_function
def compare_similarity(text1, text2):
    # nltk.download('stopwords')
    # nltk.download('punkt')
    # nltk.download('wordnet')
    # Preprocess the texts
    preprocessed_text1 = preprocess_text(text1)
    preprocessed_text2 = preprocess_text(text2)

    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([preprocessed_text1, preprocessed_text2])

    # Compute cosine similarity
    similarity = cosine_similarity(vectors[0], vectors[1])[0][0]

    return similarity


# Example usage
article1 = "This is the first news article."
article2 = "This is another news article with similar content."

similarity_score = compare_similarity(article1, article2)
print(f"Similarity score: {similarity_score}")

import tensorflow as tf
import tensorflow_hub as hub


@log_function
def compare_texts_tf(text1, text2):
    # Load the Universal Sentence Encoder module
    module_url = "https://tfhub.dev/google/universal-sentence-encoder-large/5"
    embed = hub.load(module_url)

    # Encode the texts into embeddings
    embeddings = embed([text1, text2])

    # Calculate cosine similarity
    similarity = tf.keras.losses.cosine_similarity(embeddings[0], embeddings[1]).numpy()
    return similarity
