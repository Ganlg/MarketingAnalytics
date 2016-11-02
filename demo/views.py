from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from .forms import MessageForm
from mlmodels.sentiment import SentimentModel
from tools.decorators import ajax_required

sentiment_model = None

# Create your views here.
def sentiment(request):
    return render(request, 'demo/sentiment.html')


@ajax_required
@require_POST
def ajax_sentiment(request):
    form = MessageForm(request.POST)
    if form.is_valid():
        text = form.cleaned_data['text']
        global sentiment_model
        if sentiment_model is None:
            sentiment_model = SentimentModel()
        result = int(sentiment_model.predict(text) * 100)
    return JsonResponse({'sentiment': result})

