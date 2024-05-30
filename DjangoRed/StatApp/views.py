import mysql.connector
from django.shortcuts import render
from DatasetViewApp.forms import Dataset_operation_form
from IdApp.task_id_manager import Job_types
from .db_queries import select_comment_dataset_from_ids, make_job

from wordcloud import WordCloud, STOPWORDS
import io
import base64
from nltk.tokenize import word_tokenize
import pandas as pd
import string

from IdApp.task_id_manager import get_task_id, Job_types
from DjangoRed.settings import BASE_DIR

# Create your views here.
def stat_view(request):
    stopw = STOPWORDS
    punk = list(string.punctuation)
    neg = open(BASE_DIR / "StatApp/posnag/negative-words.txt").read().split('\n')
    paz = open(BASE_DIR / "StatApp/posnag/positive-words.txt").read().split('\n')

    context = {
        "dataset_ids": [],
        "error": None,
        "downloadable": None,
        "html_embed": None,
        "stat_dict": {},
        "job_id": None,
    }

    if request.method == "GET":
        return render(request, "stat/stat.html", context = context)
    
    form = Dataset_operation_form(request)
    dataset_ids = form.get_ids_as_list()

    if not dataset_ids:
        return render(request, "stat/stat.html", context = context)

    context["dataset_ids"] = dataset_ids
    if not form.is_valid():
        context["error"] = "Unsupported dataset combination"
    
        return render(request, "stat/stat.html", context = context)
    
    if form.get_common_job_id() != Job_types.PARSE_COMMENTS:
        context["error"] = "Only user datasets can be used for statistics"
    
        return render(request, "stat/stat.html", context = context)

    table_data = select_comment_dataset_from_ids(dataset_ids)
    stat_dict = {}

    data = {'action' : 'statistical analysis', 'datasets' : dataset_ids}
    job_id = get_task_id(Job_types.STAT, data) #got job_id

    # dict
    #   {(full_name)fc231: (title, [text_mess_1; text_mess_2], upvote, pop_stat, wc_stat, string rate, % rate, pos_t, neg_t, url) , }
    
    for text_body, full_name, title, upvotes, url in table_data:
        if stat_dict.get(full_name) == None:
            stat_dict[full_name] = [title, [text_body], upvotes,'3','4','5','6','7','8', url]
        else:
            stat_dict[full_name][1].append(text_body)
   
    for full_name in stat_dict:
        #pop_stat
        stat_dict[full_name][3] = round((list(stat_dict.keys()).index(full_name))+1 / (len(stat_dict.keys())/100),2)

        #wc_stat
        list_st = ""
        for comment in stat_dict[full_name][1]:
            if comment != "[deleted]":
                list_st += ''.join(stri.strip('.!,*') + ' ' for stri in comment.replace("\n", " ").split(' '))
        WC = WordCloud(width = 450, height = 260, background_color='black', colormap='Set2', collocations=False, stopwords=stopw)
        WC.generate(list_st)
        buffer = io.BytesIO()
        WC.to_image().save(buffer, 'png')
        data64 = base64.b64encode(buffer.getvalue())
        buffer.flush()

        stat_dict[full_name][4] = data64
        
        #posneg
        df = pd.DataFrame({'text_body' : stat_dict[full_name][1]})
        df['body_tok'] = df['text_body'].str.lower()
        #nltk.download('punkt')
        df['body_tok'] = df['body_tok'].apply(word_tokenize)
        df['body_tok'] = df['body_tok'].apply(lambda x: [words for words in x if words not in punk])
        df['tok_count'] = df['body_tok'].apply(len)
        df['p_tok'] = df['body_tok'].apply(lambda x: len([words for words in x if words in paz]))
        df['n_tok'] = df['body_tok'].apply(lambda x: len([words for words in x if words in neg]))
        pos = int(df['p_tok'].sum())
        nag = int(df['n_tok'].sum())
        pos_t = df.iloc[df['p_tok'].idxmax()]['text_body']
        neg_t = df.iloc[df['n_tok'].idxmax()]['text_body']

        if (pos != 0 and nag !=0):
            per_total = pos/(nag/100)-100
        else:
            per_total = 100*pos if pos != 0 else -100*nag
        
        if per_total > 25:
            str_total = "Overwhelmingly Positive"
        elif per_total > 0:
            str_total = "Slighly Postivie"
        elif per_total == 0:
            str_total = "Neutral"
        elif per_total < -25:
            str_total = "Overwhelmingly Negative"
        elif per_total > -25:
            str_total = "Slighly Negative"

        stat_dict[full_name][5] = str_total
        stat_dict[full_name][6] = str(round(per_total,2))
        stat_dict[full_name][7] = pos_t
        stat_dict[full_name][8] = neg_t 

        params = {
            'url': stat_dict[full_name][9],
            'full_name': full_name, 
            'title': stat_dict[full_name][0],
            'upvote': stat_dict[full_name][2],  
            'word_cloud': str(data64)[2:-1],
            'neg_count': nag,
            'pos_count': pos,
            'neg_com': neg_t,
            'pos_com': pos_t, 
            'job_id': job_id
        }

        make_job(params)

        stat_dict[full_name].pop(1)
        stat_dict[full_name].pop(1)
    context['stat_dict'] = stat_dict
    context['job_id'] = job_id

    return render(request, "stat/stat.html", context = context)
