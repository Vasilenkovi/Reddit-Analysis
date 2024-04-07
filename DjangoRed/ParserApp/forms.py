from django import forms

TARGET_CHOICES = [("submissions", "submissions"), ("subreddit users", "subreddit users")]
SUBMISSION_SOURCE_CHOICES = [("submission url", "submission url"), ("subreddit", "subreddit")]
SORT_CHOICES = [("relevance", "relevance"), ("hot", "hot"), ("top", "top"), ("new", "new")]
TIME_FILTER_CHOICES = [("all", "all"), ("day", "day"), ("hour", "hour"), ("month", "month"), ("week", "week"), ("year", "year")]

class Parse_form(forms.Form):
    target = forms.ChoiceField(choices = TARGET_CHOICES, widget = forms.Select)

    #Submission parameters
    submission_source = forms.ChoiceField(choices = SUBMISSION_SOURCE_CHOICES, widget = forms.Select, initial = 0, label = "Submission source", )

    #Submission from URL
    submission_url = forms.URLField(label = "Submission source", required = True)

    #Submissions from subreddit
    subreddit_name = forms.CharField(label = "Subreddit to parse from", required = True)
    subreddit_query = forms.CharField(label = "Query inside subreddit")
    subreddit_sort = forms.ChoiceField(choices = SORT_CHOICES, widget = forms.Select, label = "Sort option", initial = 0)
    time_filter = forms.ChoiceField(choices = TIME_FILTER_CHOICES, widget = forms.Select, label = "time filter option", initial = 0)
    search_limit = forms.IntegerField(min_value = 25, initial = 25, label = "How many submissions to retrieve from subreddit")
    
    #Subreddit_users
    multi_subreddit_name = forms.CharField(label = "Subreddits to parse from", required = True)

    #Common
    comment_replace_limit = forms.IntegerField(min_value = 0, initial = 0, label = "How deep to parse threads")
    comment_replace_threshold = forms.IntegerField(min_value = 0, initial = 0, label = "Minimum depth of thread to parse deeper")



