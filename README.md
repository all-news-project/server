# All News Project Server Side

> Server Components:

| Component                                      | Description                                                                                                                                                                                                                                                                                                                                   |
|:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [```REST API```](api)                          | Python flask REST API that will be connected to the database and get the articles by different filters, in addition the API will have a component that will be connected to the database and by given article URL it will check if there are more stored articles in the database with the same subject that the NLP model already classified |
| [```Tasks scheduler```](scheduler)             | Creating the scheduled scraping tasks that will collect data / articles from websites (Batch system), by creating them in the database ```tasks``` collection                                                                                                                                                                                 |
| [```Scraping articles componenet```](scrapers) | Taking pending tasks from the database and collect articles using python selenium web scraping and insert the articles data into the database ```articles``` collection                                                                                                                                                                       |
| [```Database (MongoDB)```](db_utils)           | Store all the articles and the collecting tasks                                                                                                                                                                                                                                                                                               |
| [```NLP MODEL```](nlp_models)                  | To classify articles into clusters (same articles subjects)                                                                                                                                                                                                                                                                                   |
| [```NLP SUMMARIZER```](nlp_models)             | Summarize the articles content                                                                                                                                                                                                                                                                                                                |
