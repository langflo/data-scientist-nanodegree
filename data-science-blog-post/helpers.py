from ast import literal_eval
import itertools
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np


def parse_json(df_col):
    """
    Parses a stringified df column and returns the values for name keys as list.
    :param df_col: DataFrame column (Series)
    :return: List of extracted name values
    """
    df_col = df_col.fillna('[]').apply(literal_eval)
    df_col = df_col.apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])

    return df_col


def engineer_genre_columns(movies):
    """
    Creates a column for each genre and sets the value for a movie 1 if the genre applies and 0 if not.
    :param movies: DataFrame movies
    :return: None
    """

    def check_genres(genre_list):
        """
        Checks if a genre is in the movie genre list field.
        :param genre_list:
        :return: 1 if genre is in genre_list and 0 otherwise
        """
        try:
            if genre_list.count(g) > 0:
                return 1
            else:
                return 0
        except AttributeError:
            return 0

    # Create a set of genres from genres Series
    genres = set(itertools.chain.from_iterable(movies["genres"]))

    for g in genres:
        movies[g] = movies['genres'].apply(check_genres)


def summarize_movie_data(movies, group_by):
    """
    Groups the data and calculates aggregated measures
    :param movies: DataFrame including movie data
    :param group_by: List including DataFrame columns for grouping
    :return summary: DataFrame including grouped and aggregated measures
    """
    summary = movies.groupby(group_by).agg(
        count=('id', 'count'),
        vote_avg=('vote_average', 'mean'),
        budget_avg=('budget ($M)', 'mean'),
        revenue_avg=('revenue ($M)', 'mean'),
        profit_avg=('profit ($M)', 'mean'))

    summary['roi_avg'] = summary['profit_avg'] / summary['budget_avg']
    summary

    return summary


def plot_genres_over_time(genre_rank_decade):
    """
    Plots a bump chart for genre rankings over time
    :param genre_rank_decade: DataFrame ranking genres by number of movies by decade
    :return: None
    """
    # Set colors and theme
    colors = ['#9b59b6', '#95a5a6', '#42c070', '#9c5c2e', '#2ecc71', '#e1839d', '#0295e2', '#03012d',
              '#f0944d', '#c243cf', '#8ab8fe', '#e44586', '#ce4c29', '#75fd63', '#cea33b', '#ffc512',
              '#13eac9', '#6c7a0e', '#48bbd2', '#d1c7a1']

    sns.set(style='ticks')
    sns.set_palette(sns.color_palette(colors), n_colors=20)
    # sns.palplot(sns.color_palette(colors))

    # Plot
    fig, ax = plt.subplots(figsize=(17, 15.1))
    lines = ax.plot(genre_rank_decade, marker='o', markersize=20, linestyle='dotted', linewidth=0.5)

    # Set up legend
    lastrow = genre_rank_decade.iloc[-1, :].values
    order = np.argsort(lastrow)

    ax.legend(np.array(lines)[order], genre_rank_decade.columns[order], loc='center left',
              bbox_to_anchor=(1.025, 0.5), frameon=False, fontsize=14, labelspacing=1.8)

    # Title and axes
    ax.set_title('Movie Genres - Ranking over Time', fontsize=20)
    ax.set_xlabel('Decade', fontsize=15)
    ax.set_ylabel('Rank (# Movies)', fontsize=15)
    ax.invert_yaxis()
    ax.set_yticks(np.arange(1, 21, step=1))
    ax.set_ylim([21, 0])
    ax.set_xticks(np.arange(1870, 2020, step=10))
    ax.tick_params(axis='both', labelsize=14, labelright=True)

    plt.savefig('images/genres_over_time.png', bbox_inches="tight")


def plot_novel_comparison(movies_novel_decade, metric):
    """
    Plots a comparison between novel and non-novel based movies for metric
    :param movies_novel_decade: DataFrame including different metrics for each decade
    :param metric: String metric for comparison ('profit_average', 'vote_average', 'roi_average')
    :return: None
    """

    sns.set(style='whitegrid')

    fig, ax = plt.subplots(figsize=(17, 8))
    sns.set_palette(sns.color_palette(['#6588e4', '#BDBDBD']), n_colors=2)
    ax = sns.barplot(data=movies_novel_decade.reset_index(),
                     x='release_decade',
                     y=metric,
                     hue='is_novel_based')

    h, l = ax.get_legend_handles_labels()

    # Title, axes, legend
    if metric == 'profit_avg':
        ax.set_title('Movies novel vs. non-novel - Average Profit', fontsize=18)
        ax.set_xlabel('Decade', fontsize=14)
        ax.set_ylabel('Avg Profit ($M)', fontsize=14)
        ax.legend(h, ['non-novel', 'novel'], loc='upper left', fontsize=14)
        plt.savefig('images/profit_average.png', bbox_inches="tight")

    if metric == 'vote_avg':
        ax.set_title('Movies novel vs. non-novel - Average Vote', fontsize=18)
        ax.set_xlabel('Decade', fontsize=14)
        ax.set_ylabel('Avg Vote', fontsize=14)
        ax.legend(h, ['non-novel', 'novel'], loc='upper right', fontsize=14)
        plt.savefig('images/vote_average.png', bbox_inches="tight")

    if metric == 'roi_avg':
        ax.set_title('Movies novel vs. non-novel - Average ROI', fontsize=18)
        ax.set_xlabel('Decade', fontsize=14)
        ax.set_ylabel('Avg RoI (%)', fontsize=14)
        ax.legend(h, ['non-novel', 'novel'], loc='upper right', fontsize=14)
        plt.savefig('images/roi_average.png', bbox_inches="tight")


def plot_top_profitable_movies(top_profitable):
    """
    Plots a horizontal bar chart for top 10 profitable movies novel vs. non-novel
    :param top_profitable: DataFrame including profit information
    :return: None
    """
    colors = []

    for ind in top_profitable.index:
        if top_profitable['is_novel_based'][ind]:
            colors.append('#BDBDBD')
        else:
            colors.append('#6588e4')

    sns.set(style='whitegrid')
    fig, ax = plt.subplots(figsize=(12, 10))
    ax = sns.barplot(x='profit ($M)',
                     data=top_profitable,
                     y='title',
                     palette=colors)

    # Title and axes
    ax.set_title('Movies novel vs. non-novel - Top 10 by Profit', fontsize=18)
    ax.set_xlabel('Profit in $M', fontsize=14)
    ax.set_ylabel('', fontsize=14)

    # Legend
    grey_patch = mpatches.Patch(color='#BDBDBD', label='novel')
    blue_patch = mpatches.Patch(color='#6588e4', label='non-novel')
    plt.legend(handles=[blue_patch, grey_patch], loc='lower right', fontsize=14)

    plt.savefig('images/top_profitable.png', bbox_inches="tight")


def plot_movies_financials(movies_financials):
    """
    Plots a horizontal bar chart displaying budget, revenue and profit
    :param movies_financials: DataFrame including financial movie information
    :return: None
    """

    fig, ax = plt.subplots(figsize=(12, 10))
    sns.set(style='whitegrid')
    ax = sns.barplot(x='value',
                     data=movies_financials,
                     y='title',
                     hue='metric',
                     palette=['#6588e4', '#BDBDBD', '#FFD700'])

    # Title and axes
    ax.set_title('Movies with highest Budgets - Profitability', fontsize=18)
    ax.set_xlabel('$M', fontsize=14)
    ax.set_ylabel('', fontsize=14)

    # Legend
    ax.legend(loc='lower right', fontsize=14)

    plt.savefig('images/movie_financials.png', bbox_inches="tight")


def plot_movies_roi(movies_financials):
    """
    Plots a horizontal bar chart displaying return on investment
    :param movies_financials: DataFrame including financial movie information
    :return: None
    """

    fig, ax = plt.subplots(figsize=(12, 8))
    sns.set(style='whitegrid')
    ax = sns.barplot(x='roi (%)',
                     data=movies_financials,
                     y='title',
                     color='#6588e4')

    # Title and axes
    ax.set_title('Movies - Highest RoI', fontsize=18)
    ax.set_xlabel('RoI (%)', fontsize=14)
    ax.set_ylabel('', fontsize=14)

    plt.savefig('images/highest_roi.png', bbox_inches="tight")
