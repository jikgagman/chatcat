# chat/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import User, ChatMessage
from .forms import LoginForm
import random
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404



def enter_chat(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            nickname = form.cleaned_data['nickname']
            user, created = User.objects.get_or_create(nickname=nickname)
            request.session['user_id'] = user.id  # Store user id in session
            return redirect('chat')
    else:
        form = LoginForm()
    return render(request, 'chat/enter_chat.html', {'form': form})


def chat(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('enter_chat')
    user = User.objects.get(id=user_id)
    messages = ChatMessage.objects.all()
    return render(request, 'chat/chat.html', {'messages': messages, 'user': user})


@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data['message']
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({'error': 'User not authenticated'}, status=400)
        user = User.objects.get(id=user_id)

        # Check if the user already has a character with a position
        existing_message = ChatMessage.objects.filter(user=user).first()
        if existing_message:
            x_position = existing_message.x_position
            y_position = existing_message.y_position
        else:
            x_position = random.randint(0, 800)  # Random X position for simplicity
            y_position = random.randint(0, 400)  # Random Y position for simplicity

        # Remove all previous messages for the user
        ChatMessage.objects.filter(user=user).delete()

        chat_message = ChatMessage(user=user, message=message, x_position=x_position, y_position=y_position)
        chat_message.save()
        return JsonResponse({'user': user.nickname, 'user_id': user.id, 'message': message, 'x_position': x_position,
                             'y_position': y_position}, status=200)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@user_passes_test(lambda u: u.is_superuser)
def remove_character(request, user_id):
    user = get_object_or_404(User, id=user_id)
    ChatMessage.objects.filter(user=user).delete()
    return redirect('chat')
