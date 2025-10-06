# messaging/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from django.shortcuts import render
from .models import Message

User = get_user_model()

@login_required
def delete_user(request):
    """
    Allows the currently logged-in user to delete their account.
    Automatically triggers post_delete signal to clean up data.
    """
    user = request.user

    if request.method == "POST":
        username = user.username
        logout(request)  # log the user out first
        user.delete()    # this triggers the post_delete signal
        messages.success(request, f"Account '{username}' deleted successfully.")
        return redirect("home")  # replace 'home' with your homepage URL name

    # If GET request, render confirmation
    return render(request, "messaging/delete_user_confirm.html")

@login_required
def threaded_conversations(request):
    """
    Display all messages (and their threaded replies)
    for the current logged-in user.
    """
    # ✅ Filter messages related to this user (either sent or received)
    messages = Message.objects.filter(
        sender=request.user
    ).select_related('sender', 'receiver').prefetch_related('replies') | Message.objects.filter(
        receiver=request.user
    ).select_related('sender', 'receiver').prefetch_related('replies')

    # ✅ Recursive function to build threaded structure
    def build_thread(message):
        return {
            "id": message.id,
            "sender": message.sender.username,
            "receiver": message.receiver.username,
            "content": message.content,
            "timestamp": message.timestamp,
            "replies": [build_thread(reply) for reply in message.replies.all()]
        }

    # ✅ Only include top-level messages (those without parent)
    top_level_messages = messages.filter(parent_message__isnull=True)

    threads = [build_thread(msg) for msg in top_level_messages]

    # ✅ Render in a simple template
    return render(request, "messaging/threaded_conversations.html", {"threads": threads})


@login_required
def analytics_view(request):
    """
    View that displays messaging analytics using aggregation and annotation.
    """

    # ✅ Total messages in the system
    total_messages = Message.objects.count()

    # ✅ Messages sent per user (annotation)
    messages_per_user = (
        User.objects.annotate(sent_count=Count('sent_messages'))
        .values('username', 'sent_count')
        .order_by('-sent_count')
    )

    # ✅ Most active users — top 5
    most_active_users = messages_per_user[:5]

    context = {
        'total_messages': total_messages,
        'messages_per_user': messages_per_user,
        'most_active_users': most_active_users,
    }

    return render(request, 'messaging/analytics.html', context)