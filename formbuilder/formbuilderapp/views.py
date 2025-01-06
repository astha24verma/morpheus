from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count
from collections import Counter
import json
from .models import Form, Question, Response as FormResponse, Answer
from .forms import FormCreateForm, QuestionForm, SignUpForm
from django.contrib.auth import login
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

def form_list(request):
    """
    Display a list of all forms. If the user is authenticated, also display forms created by the user.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse or JsonResponse: The rendered list of forms or JSON data.
    """
    all_forms = Form.objects.all().order_by('-created_at')
    my_forms = None

    if request.user.is_authenticated:
        my_forms = Form.objects.filter(created_by=request.user).order_by('-created_at')

    if request.headers.get('Content-Type') == 'application/json':
        data = {
            'all_forms': list(all_forms.values()),
            'my_forms': list(my_forms.values()) if my_forms is not None else []
        }
        return JsonResponse(data)

    return render(request, 'forms/list.html', {
        'all_forms': all_forms,
        'my_forms': my_forms,
        'show_all_only': not request.user.is_authenticated
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def api_form_create(request):
    """
    Create a new form via API. Only accessible to authenticated users.
    """
    form = FormCreateForm(data=request.data)
    if form.is_valid():
        new_form = form.save(commit=False)
        new_form.created_by = request.user
        new_form.save()
        return Response({'status': 'success', 'form_id': new_form.id}, status=200)
    else:
        return Response({'status': 'error', 'errors': form.errors}, status=400)

@login_required
def web_form_create(request):
    """
    Create a new form via web. Only accessible to authenticated users.
    """
    if request.method == 'POST':
        form = FormCreateForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.created_by = request.user
            new_form.save()
            return redirect('web_form_edit', form_id=new_form.id)
    else:
        form = FormCreateForm()
    
    return render(request, 'forms/create.html', {'form': form})

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def api_form_edit(request, form_id):
    form = get_object_or_404(Form, id=form_id, created_by=request.user)
    if request.method == 'POST':
        form_data = request.data
        form.title = form_data.get('title', form.title)
        form.description = form_data.get('description', form.description)
        form.save()
        return Response({'status': 'success', 'message': 'Form updated successfully'}, status=200)
    return Response({'title': form.title, 'description': form.description}, status=200)

@login_required
def web_form_edit(request, form_id):
    form = get_object_or_404(Form, id=form_id, created_by=request.user)
    if request.method == 'POST':
        form_data = request.POST
        form.title = form_data.get('title', form.title)
        form.description = form_data.get('description', form.description)
        form.save()
        return redirect('web_form_edit', form_id=form.id)
    return render(request, 'forms/edit.html', {'form': form})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def api_form_submit(request, form_id):
    form = get_object_or_404(Form, id=form_id)
    response = FormResponse.objects.create(form=form, ip_address=request.META.get('REMOTE_ADDR'))
    for question in form.questions.all():
        answer_data = request.data.get(f'question_{question.id}')
        if answer_data:
            answer_text = json.dumps(answer_data) if question.question_type == 'checkbox' else answer_data
            Answer.objects.create(response=response, question=question, answer_text=answer_text)
    return Response({'status': 'success', 'message': 'Response submitted successfully'}, status=200)

@login_required
def web_form_submit(request, form_id):
    form = get_object_or_404(Form, id=form_id)
    if request.method == 'POST':
        response = FormResponse.objects.create(form=form, ip_address=request.META.get('REMOTE_ADDR'))
        for question in form.questions.all():
            answer_data = request.POST.getlist(f'question_{question.id}')
            if answer_data:
                answer_text = json.dumps(answer_data) if question.question_type == 'checkbox' else answer_data[0]
                Answer.objects.create(response=response, question=question, answer_text=answer_text)
        return redirect('form_thank_you', form_id=form_id)
    return render(request, 'forms/submit.html', {'form': form})

@api_view(['GET'])
@csrf_exempt
def api_form_analytics(request, form_id):
    form = get_object_or_404(Form, id=form_id)
    
    analytics_data = {}
    total_responses = FormResponse.objects.filter(form=form).count()
    
    for question in form.questions.all():
        answers = Answer.objects.filter(question=question)
        question_response_count = answers.count()
        
        if question.question_type == 'text':
            word_counts = Counter()
            for answer in answers:
                if answer.answer_text:
                    words = [word for word in answer.answer_text.split() if len(word) >= 5]
                    word_counts.update(words)
            
            top_words = word_counts.most_common(5)
            others_count = sum(count for word, count in word_counts.items() if (word, count) not in top_words)
            analytics_data[str(question.id)] = {
                'type': 'text',
                'data': top_words + [('Others', others_count)],
                'total_responses': question_response_count
            }
            
        else:
            option_counts = Counter()
            for answer in answers:
                if answer.answer_text:
                    if question.question_type == 'checkbox':
                        try:
                            selected_options = tuple(sorted(json.loads(answer.answer_text)))
                            option_counts[selected_options] += 1
                        except json.JSONDecodeError:
                            continue
                    else:
                        option_counts[answer.answer_text] += 1
            
            top_options = option_counts.most_common(5)
            others_count = sum(count for option, count in option_counts.items() if (option, count) not in top_options)
            analytics_data[str(question.id)] = {
                'type': question.question_type,
                'data': top_options + [('Others', others_count)],
                'total_responses': question_response_count
            }

    return Response({
        'form': form.title,
        'analytics': analytics_data,
        'total_responses': total_responses
    }, status=200)

@login_required
def web_form_analytics(request, form_id):
    form = get_object_or_404(Form, id=form_id, created_by=request.user)
    
    analytics_data = {}
    total_responses = FormResponse.objects.filter(form=form).count()
    
    for question in form.questions.all():
        answers = Answer.objects.filter(question=question)
        question_response_count = answers.count()
        
        if question.question_type == 'text':
            word_counts = Counter()
            for answer in answers:
                if answer.answer_text:
                    words = answer.answer_text.split()
                    word_counts.update(words)
            
            analytics_data[str(question.id)] = {
                'type': 'text',
                'data': word_counts.most_common(5),
                'total_responses': question_response_count
            }
            
        else:
            option_counts = Counter()
            for answer in answers:
                if answer.answer_text:
                    if question.question_type == 'checkbox':
                        try:
                            selected_options = json.loads(answer.answer_text)
                            for option in selected_options:
                                option_counts[option] += 1
                        except json.JSONDecodeError:
                            continue
                    else:
                        option_counts[answer.answer_text] += 1
            
            analytics_data[str(question.id)] = {
                'type': question.question_type,
                'data': [(option, count) for option, count in option_counts.items()],
                'total_responses': question_response_count
            }

    return render(request, 'forms/analytics.html', {
        'form': form,
        'analytics': analytics_data,
        'total_responses': total_responses
    })

def form_thank_you(request, form_id):
    """
    Display a thank you page after form submission.

    Args:
        request (HttpRequest): The request object.
        form_id (int): The ID of the form.

    Returns:
        HttpResponse: Renders the thank you page.
    """
    form = get_object_or_404(Form, id=form_id)
    return render(request, 'forms/thank_you.html', {'form': form})

def signup(request):
    """
    Handle user signup.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Redirects to form list page after successful signup.
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('form_list')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})