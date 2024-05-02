import praw
from praw.models import MoreComments
import os
import csv
from collections import defaultdict
import pandas as pd


def init_reddit():
    reddit = praw.Reddit(
        client_id=os.environ.get("REDDIT_CLIENT_ID", ""),
        client_secret=os.environ.get("REDDIT_CLIENT_SECRET", ""),
        password=os.environ.get("REDDIT_PASSWORD", ""),
        user_agent=os.environ.get("REDDIT_USER_AGENT", ""),
        username=os.environ.get("REDDIT_USERNAME", ""),
    )
    print(f"Successfully logged in as: {reddit.user.me()}")
    return reddit


def generate_submission_csv(reddit, filename, subreddit_name="TrueCrime", limit=25):
    column_names = [
        "title",
        "id",
        "permalink",
        "name",
        "created_utc",
        "selftext",
        "score",
        "upvote_ratio",
    ]

    with open(filename, "w", newline="") as csvfile:
        headerwriter = csv.writer(csvfile)
        headerwriter.writerow(column_names)

    subreddit = reddit.subreddit(subreddit_name)

    for submission in subreddit.top(limit=limit):
        data = defaultdict(lambda: "")
        data["title"] = submission.title
        data["id"] = submission.id

        data["permalink"] = submission.permalink
        try:
            data["name"] = submission.author.name
        except AttributeError:
            pass
        data["created_utc"] = submission.created_utc
        data["selftext"] = submission.selftext.replace("\n", " ")
        data["score"] = submission.score
        data["upvote_ratio"] = submission.upvote_ratio

        with open(filename, "a", newline="") as csvfile:
            headerwriter = csv.writer(csvfile)
            headerwriter.writerow([data[column] for column in column_names])


def clean_comment_body(body):
    strings_to_remove = ["\n", "", "[deleted]", "[removed]"]
    for remove_str in strings_to_remove:
        body = body.replace(remove_str, "")
    return body


def generate_comments_csv(reddit, submission_ids, filename):
    column_names = [
        "post_id",
        "id",
        "permalink",
        "name",
        "body",
        "score",
        "created_utc",
    ]

    with open(filename, "w", newline="",encoding='utf-8') as csvfile:
        headerwriter = csv.writer(csvfile)
        headerwriter.writerow(column_names)

    for submission_id in submission_ids:
        submission = reddit.submission(submission_id)
        submission.comments.replace_more(limit=0)
        for top_level_comment in submission.comments:
            if isinstance(top_level_comment, MoreComments):
                continue

            data = defaultdict(lambda: "")
            data["post_id"] = submission_id
            data["id"] = top_level_comment.id
            data["permalink"] = top_level_comment.permalink
            try:
                data["name"] = top_level_comment.author.name
            except AttributeError:
                pass

            data["body"] = clean_comment_body(top_level_comment.body)
            data["score"] = top_level_comment.score
            data["created_utc"] = top_level_comment.created_utc
            with open(filename, "a", newline="",encoding='utf-8') as csvfile:
                headerwriter = csv.writer(csvfile)
                headerwriter.writerow([data[column] for column in column_names])


if __name__ == "__main__":
    reddit = init_reddit()
    # generate_submission_csv(reddit, "truecrime_submissions.csv")
    submission_csv = pd.read_csv("truecrime_submissions.csv")
    submission_ids = submission_csv["id"].tolist()
    generate_comments_csv(reddit, submission_ids, "truecrime_comments.csv")
