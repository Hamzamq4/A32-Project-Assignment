import praw
from datetime import datetime, timezone
import csv

# Replace these with your actual credentials
CLIENT_ID = "iXwJeKl0KJXTptbjW8ZoJg"
CLIENT_SECRET = "iGz4rJZ7R_l33esEkO5S37Sg6J0PEA"
USER_AGENT = "keyword_search_script by u/Other_Dig1282"

def fetch_all_comments(submission):
    """
    Fetch all comments from a submission and return them as a single string (one line).
    """
    submission.comments.replace_more(limit=None)
    all_comments = []
    for comment in submission.comments.list():
        # Replace newlines in comment body with spaces
        cleaned_body = comment.body.replace('\n', ' ')
        all_comments.append(cleaned_body)
    # Join all comments with a space instead of newlines
    return " ".join(all_comments)

def search_with_time_filter(subreddit_name, keyword, time_filter='year', limit=2000, filename="default.csv"):
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT
    )
    subreddit = reddit.subreddit(subreddit_name)
    
    print(f"Searching for '{keyword}' in r/{subreddit_name} with time_filter='{time_filter}'...")

    # Collect all results
    all_results = list(subreddit.search(keyword, sort='relevance', time_filter=time_filter, limit=limit))
    
    if not all_results:
        print("No posts found at all.")
        return

    print("\nAll Retrieved Posts:")
    rows = []
    for submission in all_results:
        submission_date = datetime.fromtimestamp(submission.created_utc, tz=timezone.utc)
        post_url = f"https://www.reddit.com{submission.permalink}"
        content = submission.selftext if submission.selftext else "[No textual content]"

        print(f"Title: {submission.title}")
        print(f"Created (UTC): {submission_date.isoformat()}")
        print(f"URL: {submission.url}")
        print(f"Reddit Post URL: {post_url}")
        print("Content:")
        print(content)
        
        # Fetch all comments for this submission
        print("Fetching comments...")
        comments_text = fetch_all_comments(submission)
        print(f"Number of comments fetched: {len(comments_text.split())}")
        print("-" * 40)
        
        # Prepare row for CSV
        rows.append({
            "title": submission.title,
            "created_utc": submission_date.isoformat(),
            "reddit_post_url": post_url,
            "content": content,
            "score": submission.score,
            "author": str(submission.author),
            "url": submission.url,
            "comments": comments_text
        })

    # Save all results to CSV
    csv_filename = filename
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["title", "created_utc", "reddit_post_url", "content", "score", "author", "url", "comments"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nData saved to {csv_filename}")

if __name__ == "__main__":
    # Example usage
    search_with_time_filter("Soccer", "Mbappe transfer", time_filter='year', limit=20, filename="Mbappe_transfer.csv")
    search_with_time_filter("Soccer", "Olmo transfer", time_filter='year', limit=20, filename="Olmo_transfer.csv")
    search_with_time_filter("Soccer", "Diaby transfer", time_filter='year', limit=20, filename="Diaby_transfer.csv")
    search_with_time_filter("Soccer", "Yoro transfer", time_filter='year', limit=20, filename="Yoro_transfer.csv")
    search_with_time_filter("Soccer", "Solanke transfer", time_filter='year', limit=20, filename="Solanke_transfer.csv")
    search_with_time_filter("Soccer", "De Ligt transfer", time_filter='year', limit=20, filename="Deligt_transfer.csv")
    search_with_time_filter("Soccer", "Douglas Luiz transfer", time_filter='year', limit=20, filename="DL_transfer.csv")
    search_with_time_filter("Soccer", "Julian Alvarez transfer", time_filter='year', limit=20, filename="Alvarez_transfer.csv")
    search_with_time_filter("Soccer", "Pedro Neto transfer", time_filter='year', limit=20, filename="Pedro_transfer.csv")
