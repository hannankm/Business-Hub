from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Question, Response, Vote
from .forms import QuestionForm, ResponseForm
# Create your views here.

# Get all forum questions (with filter, sort, limit, search)
def discussion_forum(request):
    questions = Question.objects.all()

    # Filtering by tag
    tag = request.GET.get('tag')
    if tag:
        questions = questions.filter(tags__name=tag)

    # Sorting
    sort = request.GET.get('sort', 'date_posted')
    if sort == 'views_count':
        questions = questions.order_by('-views_count')
    elif sort == '-views_count':
        questions = questions.order_by('views_count')
    elif sort == 'replies_count':
        questions = questions.order_by('-replies_count')
    elif sort == '-replies_count':
        questions = questions.order_by('replies_count')
    elif sort == 'date_posted':
        questions = questions.order_by('-date_posted')
    elif sort == '-date_posted':
        questions = questions.order_by('date_posted')

    # Search functionality
    query = request.GET.get('search')
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
    else:
        form = ResponseForm()
    return render(request, 'discussion/question.html', {'form': form, 'question': question})




def question_detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.method == 'GET':
        question.views_count += 1
        question.save()

    if request.method == 'POST':
        response_id = request.POST.get('response_id')
        vote_type = request.POST.get('vote_type')
        if response_id and vote_type in ['upvote', 'downvote']:
            response = get_object_or_404(Response, pk=response_id)
            user = request.user

            # Check if the user has already voted on this response
            existing_vote = Vote.objects.filter(user=user, response=response).exists()
            if not existing_vote:
                if vote_type == 'upvote':
                    response.upvotes += 1
                else:
                    response.downvotes += 1
                response.save()
                Vote.objects.create(user=user, response=response, type=vote_type == 'upvote')

    sort_by = request.GET.get('sort_by', 'upvotes')
    if sort_by == 'downvotes':
        responses = question.response_set.all().order_by('-downvotes')
    else:
        responses = question.response_set.all().order_by('-upvotes')

    return render(request, 'discussion/question.html', {
        'question': question,
        'responses': responses,
    })