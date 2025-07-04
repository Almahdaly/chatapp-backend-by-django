from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from django.utils import timezone

# Create your views here.
# def chat(request):
#     pass

@login_required
def chat_view(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(user=request.user, content=content)
            return redirect('chat:chat')  # بعد الإرسال نعيد تحميل الصفحة

    messages = Message.objects.filter(deleted_at__isnull=True).order_by('created_at')
    return render(request, 'chat.html', {'messages': messages})


@login_required
def delete_message(request, message_id):
    message = Message.objects.get(id=message_id)
    if message.user == request.user:
        message.deleted_at = timezone.now()
        message.save()
    return redirect('chat:chat')