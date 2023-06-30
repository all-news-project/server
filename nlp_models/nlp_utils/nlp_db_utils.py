# from transformers import DistilBertTokenizer, DistilBertModel
#
# from db_driver.db_objects.article import Article
# from db_driver.db_objects.cluster import Cluster
# from db_driver.utils.consts import DBConsts
# from logger import get_current_logger, log_function
# from nlp_models.nlp_utils.cluster_utils import cluster_similarity
# from server_utils.db_utils.cluster_utils import ClusterUtils
#
# from db_driver import get_current_db_driver
# from db_driver.db_objects.article import Article
# from db_driver.db_objects.cluster import Cluster
# from logger import get_current_logger, log_function
# from nlp_models.exceptions import SimilarityNotFoundException
# from nlp_models.nlp_utils.nlp_utils import Nlp_Utils

#
# class NlpDBUtils:
#     def __init__(self):
#         self.logger = get_current_logger()
#         self._db = get_current_db_driver()
#         self.cluster_utils = ClusterUtils()
#         self.nlp_utils = Nlp_Utils()
#
#     @log_function
#     def classify_article(self, clusters: list[Cluster], article: Article) -> bool:
#         counter = 0
#         max_topic = None
#         max_sim = 0
#         for cluster in clusters:
#             # TODO: check cluster websites
#             if article.domain not in cluster.websites:
#                 self.logger.debug(f"checking similarity in cluster {cluster.cluster_id}")
#                 sim_rate = cluster_similarity(cluster.cluster_id, article.article_id)
#                 if sim_rate > max_sim:
#                     counter = counter + 1
#                     max_topic = cluster
#                     max_sim = sim_rate
#         if max_sim > 0:
#             # max_topic.articles_id.append(article.article_id)
#             self.cluster_utils.add_article_to_cluster(max_topic.cluster_id, article.article_id, article.domain)
#             self.logger.info(f"Added article to cluster {max_topic.cluster_id}")
#             return True
#         else:
#             try:
#                 self.logger.debug("Could not find cluster, creating new cluster")
#                 id = self.cluster_utils.create_new_cluster(article)
#                 return True
#             except Exception as e:
#                 self.logger.error(f"Could not create new cluster - {str(e)}")
#                 return False
#
#     """This function uses the DistilBert pretrained model by valurank in order to categorize articles."""
#
#     @log_function
#     def categorize_article(self, article: Article):
#         try:
#             self.logger.debug("Categorizing article")
#             tokenizer = DistilBertTokenizer.from_pretrained('finetuned-distilbert-news-article-categorization')
#             model = DistilBertModel.from_pretrained("finetuned-distilbert-news-article-categorization")
#             encoded_input = tokenizer.encode(article.content, return_tensors='pt')
#             output = model(**encoded_input)
#             self.logger.info(f"Assigning category {output} to article {article.article_id}")
#             return output
#
#         except Exception as e:
#             self.logger.error(f"Failed to categorize article {article.article_id}")
#             return None
#
#     @log_function
#     def cluster_similarity(self, cluster_id: str, new_article_id: str) -> float:
#         cluster = self._db.get_one(DBConsts.CLUSTER_TABLE_NAME, {"cluster_id": cluster_id})
#         new_article = self._db.get_one(DBConsts.ARTICLE_TABLE_NAME, {"article_id", new_article_id})
#         main_article = self._db.get_one(DBConsts.ARTICLE_TABLE_NAME, {"article_id": cluster.main_article_id})
#         sim_rate = self.nlp_utils._transformers_similarity([main_article.article_content, new_article.content])
#
#         if sim_rate > 60:
#             avg_rate = self._check_avg_cluster_sim(cluster, new_article)
#             if sim_rate > 75 and avg_rate > 60:
#                 self.logger.debug(f"High similarity with article,average{avg_rate}")
#             elif sim_rate > 60 and avg_rate > 70:
#                 self.logger.debug(f"Low similarity with article,average{avg_rate}")
#             final_result = (avg_rate + sim_rate) / 2
#             self.logger.debug(f"similarity rate to cluster is {final_result}")
#             return final_result
#         else:
#             desc = f"Error Similarity rate {sim_rate}, Similarity not found"
#             self.logger.debug(f"Similarity not found in {cluster.cluster_id}")
#             raise SimilarityNotFoundException(desc)
#
#     @log_function
#     def _check_avg_cluster_sim(self, articles_id: list[str], new_article: Article):
#         avg_rate = 0
#         articles = self._db.get_many(DBConsts.ARTICLE_TABLE_NAME, {"article_id": articles_id})
#         for article in articles:
#             avg_rate = avg_rate + self.nlp_utils._transformers_similarity([new_article, article.summary])
#         avg_rate = avg_rate / len(articles)
#         return avg_rate
