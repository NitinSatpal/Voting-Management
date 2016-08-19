from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import auth
from .models import Question, Voter, Choice
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
import datetime


# Create your views here.

#index page for the polls where all questions will be listed
def index(request):
	# if user is not loggedin then redirect user to login page first before taking the poll
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/accounts/login/?next=%s' %request.path)

	# fetch all questions in order to show to the user for polling
	latest_questions = Question.objects.order_by('-pub_date')
	context = {'latest_questions':latest_questions}
	
	return render(request, 'pollmanagement/index.html', context)

#each question's details page
def details(request, question_id):
	# get the question and count from Voter model to find whether the voting was already done
	question = get_object_or_404(Question, pk=question_id)
	num_results = Voter.objects.filter(user=request.user, poll=question).count()

	# if the user has already voted for this poll, restric the voting
	if num_results == 1:
		# set alreadyvoted to true and redirect to details page
		isAlreadyVoted = 'true'
		return render(request, 'pollmanagement/detail.html', {'question': question,'error_message': "Sorry, but you have already voted.", 'isAlreadyVoted': isAlreadyVoted})
	
	# if this is the first time user is voting for this poll, allow the user and redirect to details page
	return render(request, 'pollmanagement/detail.html', {'question': question})

#each questions result page after the poll is done
def result(request, question_id):
	# get the question in order to fetch the results in result page
	question = get_object_or_404(Question, pk=question_id)

	# redirect to results page
	return render(request, 'pollmanagement/result.html', {'question' :question})

#Voting page for each question
def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		# the seclected choice will be recorded
		selected_choice = question.choice_set.get(pk = request.POST['choice'])
	except:
		# if user has not selected the choice and cliked on vote
		return render(request, 'pollmanagement/detail.html', {'question': question, 'error_message': "Please select a choice"})
	else:
		selected_choice.votes += 1
		selected_choice.save()

		# checking whether the user has already been voted the current poll, if not mark as voted
		num_results = Voter.objects.filter(user=request.user, poll=question).count()
		if num_results != 1:
			voter = Voter(poll=question, user=request.user)
			voter.save()
		
		# Redirect to the result page of this poll
		return HttpResponseRedirect(reverse('polls:result', args=(question.id,)))

#Login of the user
def login_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        # Redirect to a success page.
        return HttpResponseRedirect("/accounts/loggedin/")
    else:
        # Show an error page
        return HttpResponseRedirect("/account/invalid/")

#logout of the user
def logout_view(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/")

#profile page for the user
def profile(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/accounts/login/?next=%s' %request.path)
	return render(request, 'account/profile.html')


#homepage for the app
def homepage(request):
	return render(request, 'pollmanagement/homepage.html')

# registration of the user
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {
        'form': form,
    })

# about us page
def about(request):
	return render(request, 'pollmanagement/about.html')

# contact us page
def contact(request):
	return render(request, 'pollmanagement/contact.html')

# show results to admin
def showresults(request):
	latest_questions = Question.objects.order_by('-pub_date')
	context = {'latest_questions':latest_questions}
	return render(request, 'pollmanagement/showResults.html', context)

def addPoll(request):
	return render(request, 'pollmanagement/addPolls.html')

# add polls
@transaction.non_atomic_requests
def commitPoll(request):
	question = Question(question_text = request.POST.get('poll'), pub_date = datetime.datetime.now())
	question.save()
	choices = []

	choices.append(request.POST.get('choiceOne'))
	choices.append(request.POST.get('choiceTwo'))
	choices.append(request.POST.get('choiceThree'))
	choices.append(request.POST.get('choiceFour'))

	for choice in choices:
		entry = Choice(question = question, choice_text = choice, votes = 0)
		entry.save()

	transaction.commit()

	return render(request, 'pollmanagement/polladdedsuccessfully.html')