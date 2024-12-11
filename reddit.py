import praw
from datetime import datetime, timezone


def search_subreddit_with_date_range(subreddit_name, keyword, start_date, end_date, max_results=50):
    """
    Search for a given keyword within a specified subreddit and filter results by a date range.
    
    :param subreddit_name: str - The name of the subreddit (e.g., 'python')
    :param keyword: str - The keyword or phrase you want to search for
    :param start_date: datetime - Start of the date range (inclusive)
    :param end_date: datetime - End of the date range (inclusive)
    :param max_results: int - The maximum number of results to fetch before filtering by date.
                              Increase this if you are not getting enough matches.
    """
    # Convert datetimes to timestamps (UTC)
    start_timestamp = start_date.replace(tzinfo=timezone.utc).timestamp()
    end_timestamp = end_date.replace(tzinfo=timezone.utc).timestamp()
    

    # Initialize Reddit instance
    reddit = praw.Reddit(
        client_id="iXwJeKl0KJXTptbjW8ZoJg",
        client_secret="iGz4rJZ7R_l33esEkO5S37Sg6J0PEA",
        user_agent="keyword_search_script by u/Other_Dig1282"
    )
    
    # Access the subreddit
    subreddit = reddit.subreddit(subreddit_name)
    
    # Perform the search (we will fetch results sorted by new, trying to get chronological order)
    # Note: `time_filter='all'` to not restrict by Reddit's predefined time filters.
    # If you want only recent results, consider `time_filter='week'` or `time_filter='month'`.
    results = []
    print(f"Searching for '{keyword}' in r/{subreddit_name} and filtering by date range...")
    for submission in subreddit.search(keyword, sort='new', time_filter='all', limit=max_results):
        # submission.created_utc is a float representing seconds since Unix epoch
        submission_date = datetime.fromtimestamp(submission.created_utc, tz=timezone.utc)
        
        if start_timestamp <= submission.created_utc <= end_timestamp:
            # This submission falls within the specified date range
            results.append({
                'title': submission.title,
                'url': submission.url,
                'score': submission.score,
                'created_utc': submission.created_utc,
                'date': submission_date.isoformat()
            })
    
    # Print filtered results
    for res in results:
        print(f"Title: {res['title']}")
        print(f"URL: {res['url']}")
        print(f"Score: {res['score']}")
        print(f"Date: {res['date']}")
        print("-" * 40)
    
    # If no results matched the criteria
    if not results:
        print("No posts found in the given date range.")


if __name__ == "__main__":
    # Define the subreddit and the keyword you want to search for
    sub_name = "soccer"
    search_term = "Guardiola"
    
    # Define your date range (UTC)
    # For example, search between January 1, 2023 and February 1, 2023 (inclusive)
    start = datetime(2025, 11, 30)
    end = datetime(2023, 12, 6)
    
    search_subreddit_with_date_range(sub_name, search_term, start, end, max_results=100)

