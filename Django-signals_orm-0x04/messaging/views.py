# messaging/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import get_user_model, logout

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
    from django.shortcuts import render
    return render(request, "messaging/delete_user_confirm.html")
