from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Question, Response
from .forms import QuestionForm, ResponseForm
# Create your views here.

# Get all forum questions (with filter, sort, limit, search)
def discussion_forum(request):
    questions = Question.objects.all()

    # Filtering by tag
    tag = request.GET.get('tag')
    # if tag:
    #     questions = questions.filter(tags__name=tag)

    # Sorting
    sort = request.GET.get('sort', 'date_posted')
    if sort == 'views':
        questions = questions.order_by('-views_count')
    elif sort == 'replies':
        questions = questions.order_by('-replies_count')
    else:
        questions = questions.order_by('-date_posted')

    # Search functionality
    query = request.GET.get('q')
    if query:
        questions = questions.filter(Q(title__icontains=query) | Q(content__icontains=query))

    # Paginating results
    limit = request.GET.get('limit', 10)  # Default limit is 10
    paginator = Paginator(questions, limit)
    page_number = request.GET.get('page', 1)  # Default page is 1
    page_obj = paginator.get_page(page_number)

    return render(request, 'discussion/discussion.html', {
        'page_obj': page_obj,
        'tag': tag,
        'sort': sort,
        'query': query
    })
# create question
def create_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            # form.save_m2m()  # Save the tags
            return redirect('discussion_forum')
    else:
        form = QuestionForm()
    return render(request, 'discussion/addquestion.html', {'form': form})

def create_response(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.user = request.user
            response.question = question
            response.save()
            question.replies_count += 1
            question.save()
            return redirect('question_detail', question_id=question.id)
    return render(request, 'discussion/create_response.html', {'form': form, 'question': question})

def update_question(request):
    return

def delete_question(request):
    return

def update_response(request):
    return 

def delete_response(request):
    return 


def question_detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    responses = question.response_set.all().order_by('-date')

    # Paginate responses
    paginator = Paginator(responses, 5)  # Display 5 responses per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    form = ResponseForm()

    return render(request, 'discussion/question.html', {'question': question, 'page_obj': page_obj, 'response_form':form })

def search_question(request):
    return 