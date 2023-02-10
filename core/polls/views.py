from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from polls.models import Choice, Question


def index(request):
    questions = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
    return render(request, 'polls/index.html', {'questions': questions})


def detail(request, question_id):
    try:
        question = Question.objects.filter(pub_date__lte=timezone.now()).prefetch_related('question_choices').get(id=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})


def vote(request, question_id):
    try:
        question = Question.objects.filter(pub_date__lte=timezone.now()).get(id=question_id)
        selected_choice = question.question_choices.get(id=request.POST['choice'])
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })

    selected_choice.votes += 1
    selected_choice.save()

    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def results(request, question_id):
    try:
        question = Question.objects.filter(pub_date__lte=timezone.now()).prefetch_related('question_choices').get(id=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/results.html', {'question': question})