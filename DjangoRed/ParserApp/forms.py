from typing import Any
from django import forms
from django.urls import reverse

SORT_CHOICES = [("relevance", "relevance"), ("hot", "hot"), ("top", "top"), ("new", "new")]
TIME_FILTER_CHOICES = [("all", "all"), ("day", "day"), ("hour", "hour"), ("month", "month"), ("week", "week"), ("year", "year")]

class Common_parsing_form(forms.Form):
    search_limit = forms.IntegerField(min_value = 25, initial = 25, label = "How many submissions to retrieve from subreddit", required=False)
    comment_replace_limit = forms.IntegerField(min_value = 0, initial = 0, label = "How deep to parse threads")
    comment_replace_threshold = forms.IntegerField(min_value = 0, initial = 0, label = "Minimum depth of thread to parse deeper")

class Submission_parsing_form(Common_parsing_form):
    submission_url = forms.URLField(label = "Submission source", required = True)

    form_type = forms.CharField(initial="comment_submission", widget=forms.HiddenInput)

    def clean(self) -> dict[str, Any]:
        clean = super().clean()
        clean['submission_url'] = [i for i in clean['submission_url'].split(";") if i]

        return clean


class Subreddit_parsing_form(Common_parsing_form):
    subreddit_name = forms.CharField(label = "Subreddit to parse from", required = True)
    subreddit_query = forms.CharField(label = "Query inside subreddit", required = False)
    subreddit_sort = forms.ChoiceField(choices = SORT_CHOICES, widget = forms.Select, label = "Sort option", initial = 0)
    time_filter = forms.ChoiceField(choices = TIME_FILTER_CHOICES, widget = forms.Select, label = "time filter option", initial = 0)
    
    form_type = forms.CharField(initial="comment_subreddit", widget=forms.HiddenInput)

class Subreddit_users_parsing_form(Common_parsing_form):
    multi_subreddit_name = forms.CharField(label = "Subreddits to parse from", required = True)
    subreddit_sort_exclusive = forms.ChoiceField(choices = SORT_CHOICES[1:], widget = forms.Select, label = "Sort option", initial = 0)
    
    form_type = forms.CharField(initial="users", widget=forms.HiddenInput)
    
    def clean(self) -> dict[str, Any]:
        clean = super().clean()
        clean['multi_subreddit_name'] = [i for i in clean['multi_subreddit_name'].split(";") if i]

        return clean