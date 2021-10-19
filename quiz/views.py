from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from .models import Questions, Score
from .forms import QuizForm
from users.decorators import unauthorised_user

User = get_user_model()


@login_required
def welcome(request):
    return render(request, 'quiz/welcome.html')


@login_required
def questions(request):
    questions = Questions.objects.all()
    context = {'questions': questions}
    return render(request, 'quiz/quiz.html', context)


class Quiz(LoginRequiredMixin, View):
    def get(self, request):
        get_questions = Questions.objects.all()
        questions = []
        data = {}
        for question in get_questions:
            ques = {
                'id': question.id,
                'question': question.question,
                'option1': question.option1,
                'option2': question.option2,
                'option3': question.option3,
                'option4': question.option4,
                'answer': question.answer,
            }
            questions.append(ques)
        data['questions'] = questions
        return JsonResponse(data)


score = 0


@login_required
def answers(request):
    questions = Questions.objects.all()
    global score
    for question in questions:
        if request.method == 'POST':
            correct_answer = question.answer
            entered_answer = request.POST.get(str(question.id))
            if entered_answer == correct_answer:
                score += 1
    user_score = Score(user=request.user, score=score)
    user_score.save()
    context = {'score': score}
    return render(request, 'quiz/answer.html', context)


def review(request):
    global score
    usr = User.objects.all()
    context = {'score': score, 'usr': usr}
    return render(request, 'quiz/review.html', context)


def certificate(request):
    global score
    context = {'score': score}
    return render(request, 'quiz/certificate.html', context)


@login_required
def check(request):
    question = Questions.objects.all()
    user = request.user
    context = {'question': question, 'user': user}
    return render(request, 'quiz/check.html', context)


def studselect(request):
    return render(request, 'quiz/studselect.html')


def leader(request):
    adr = Questions.objects.all()
    usr = User.objects.all()
    context = {'usr': usr, 'adr': adr}
    return render(request, 'quiz/leader.html', context)


@login_required
@unauthorised_user
def add_question(request):
    if request.method == 'POST':
        question = request.POST['question']
        option1 = request.POST['option1']
        option2 = request.POST['option2']
        option3 = request.POST['option3']
        option4 = request.POST['option4']
        answer = request.POST['answer']

        Questions.objects.create(question=question, option1=option1, option2=option2, option3=option3, option4=option4, answer=answer)
        context = {
            'question': question,
            'option1': option1,
            'option2': option2,
            'option3': option3,
            'option4': option4,
            'answer': answer,
        }
        return render(request, 'quiz/questions.html', context)
    return render(request, 'quiz/add_questions.html')

'''
def add_question(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            context = {
                'question': form.cleaned_data['question'],
                'option1': form.cleaned_data['option1'],
                'option2': form.cleaned_data['option2'],
                'option3': form.cleaned_data['option3'],
                'option4': form.cleaned_data['option4'],
                'answer': form.cleaned_data['answer'],
            }

            return render(request, 'quiz/questions.html', context)

    else:
        form = QuizForm()
    return render(request, 'quiz/add_questions.html', {'form': form})
'''


@login_required
@unauthorised_user
def all_questions(request):
    questions = Questions.objects.all().order_by('pk')
    return render(request, 'quiz/all_questions.html', {'questions': questions})


@login_required
@unauthorised_user
def delete_questions(request, id):
    question = get_object_or_404(Questions, id=id)
    if request.method == 'POST':
        ask = request.POST['ask']
        if ask == 'Yes':
            question.delete()
            return redirect('/quiz/all_questions/')
        elif ask == 'No':
            return redirect('/quiz/all_questions/')
    return render(request, 'quiz/delete_question.html', {'question': question})


'''
def delete_questions(request, id):
    question = get_object_or_404(Questions, id=id)

    if request.method == 'POST':
        if request.POST.get('yes') == 'Yes':
            question.delete()
            return HttpResponseRedirect('/quiz/all_questions/')
        else:
            return HttpResponseRedirect('/quiz/all_questions/')
    return render(request, 'quiz/delete_question.html', {'question': question})
'''


'''
lst = []
user_answer = []
answers = Questions.objects.all()
anslist = []
correct_answers = []

for i in answers:
    anslist.append(i.answer)
    correct_answers.append(i.answer)
print('correct ans = ', correct_answers)


def index(request):
    all_questions = Questions.objects.order_by('pk')
    paginator = Paginator(all_questions, 1)
    page = request.GET.get('page')
    try:
        questions = paginator.get_page(page)
    except PageNotAnInteger:
        questions = paginator.get_page(1)
    except EmptyPage:
        questions = paginator.get_page(paginator.num_pages)

    # get answers here using request.POST
    if request.method == 'POST':
        x = request.POST['name']
        user_answer.append(x)
    print(user_answer)
    return render(request, 'quiz/index.html', {'questions': questions})


@login_required
def result(request):
    score = 0
    for i in range(len(user_answer)):
        if user_answer[i] == correct_answers[i]:
            score += 1
    print(score)
    return render(request, 'quiz/result.html', {'score': score, 'user_answer': user_answer})


def save_ans(request):
    if request.method == 'POST':
        ans = request.POST['ans']
        lst.append(ans)


def welcome(request):
    lst.clear()
    return render(request, 'quiz/welcome.html')


'''


'''
get all correct answers in a list
get all users answers
compare both answers
'''


'''
def result(request):
    score = 0
    for i in range(len(lst)):
        if lst[i] == anslist[i]:
            score += 1
    return render(request, 'quiz/result.html', {'score': score, 'lst': lst})

def save_ans(request):
    ans = request.GET['ans']
    lst.append(ans)

'''