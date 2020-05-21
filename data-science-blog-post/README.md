# Project 1: Write a Data Science Blog Post

### Project Motivation

Movie entertainment is a big business all over the world and as part of Udacity's Data Scientist Nanodegree I am going 
to investigate a movie dataset found on [Kaggle](https://www.kaggle.com/rounakbanik/the-movies-dataset), originally sourced from 
[TMDB](https://www.themoviedb.org/).

Therefor I am going to answer following questions:

1. How have movie genres evolved over time?
2. How do novel based movies compare to non-novel based movies?
3. Which movies are the most expensive ones ever made? Did the investment pay off?
4. Which movies have the best return on investment?

### Requirements

The project should run with libraries included in the Anaconda distribution. Following main libraries have been used:

- Python 3.8.2
- numpy 1.13.3
- pandas 0.25.3
- seaborn 0.10.0
- matplotlib 0.8.4

### Files in the Repository

- `Data_Science_Blog_Post.ipynb:` Jupyter notebook containing the analysis of the project
- `Data_Science_Blog_Post.html:` Jupyter notebook saved as HTML file
- `helpers.py:` Python file containing additional code for the analysis

**data directory**

- `keywords.csv:` CSV file containing keyword information for movies
- `movies_metadata.csv:` CSV file containing all basic information for movies

**images directory**

Output folder for the visuals of the analysis

- `genres_over_time.png:` Bump chart showing genre development over time
- `highest_roi.png:` Bar chart showing movies with highest return on investment
- `movie_financials.png:` Bar chart showing budget, revenue and profit information for movies with the highest budget
- `profit_average.png:` Bar chart comparing average profit by decade for novel vs. non-novel based movies
- `top_profitable.png:` Bar chart showing top 10 profitable movies and highlighting if it is novel or non-novel
- `vote_average.png:` Bar chart showing average TMDB vote for novel vs. non-novel based movies

### Results:
Please find my summary for a non-technical audience in a blog post [here](https://medium.com/@langflo/once-upon-a-time-in-hollywood-78502cc290e9).

### Acknowledgements:
The data for the project is available on [Kaggle](https://www.kaggle.com/rounakbanik/the-movies-dataset) and was prepared by Rounak Banik. The original source is 
[The Movie Database](https://www.themoviedb.org/).   
Thanks to Udacity for a great project. 