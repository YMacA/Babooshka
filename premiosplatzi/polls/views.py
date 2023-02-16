from django.urls  import reverse
from django.shortcuts import render, get_object_or_404
from django.views import generic
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from .models import Choice, Question

code = """
def index(request):
    lastes_question_list = Question.objects.all()
    return render(request, "polls/index.html", {
        "lastes_question_list": lastes_question_list
    })
    #return HttpResponse("hello world oruguita") 


def detail(request, question_id):
    #return HttpResponse(f"estas viendo la pregunta {question_id}")
    #question = Question.objects.get(pk=question_id)
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html",{
        "question": question
    })

def results(request, question_id):
    #return HttpResponse(f"estas viendo los resultados de la pregunta nro {question_id}")
    question =  get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {
        "question": question
    })

"""
class IndexView (generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "lastes_question_list"
    def get_queryset(self):
        """return  the last five published questions"""
        return Question.objects.order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

class ResultView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def vote(request, question_id):
    #return HttpResponse(f"estas votando por la pregunta nro {question_id}")
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html",{
            "question": question,
            "error_message": "no elejiste ninguna opcion"
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
