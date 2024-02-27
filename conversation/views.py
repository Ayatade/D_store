# Import necessary modules and classes
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from item.models import Item
from .forms import ConversationMessageForm
from .models import Conversation

# Use the login_required decorator to ensure only authenticated users can access the view
@login_required
def new_conversation(request, item_pk):
    # Retrieve the item based on its primary key or raise a 404 error if not found
    item = get_object_or_404(Item, pk=item_pk)

    # Redirect the user to the dashboard if they are the creator of the item
    if item.created_by == request.user:
        return redirect('dashboard:index')
    
    # Check for existing conversations related to the item and involving the current user
    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])

    # Redirect to the detail view of the first existing conversation if it exists
    if conversations:
        return redirect('conversation:detail', pk=conversations.first().id)

    # Handle form submission
    if request.method == 'POST':
        # Initialize the form with the submitted data
        form = ConversationMessageForm(request.POST)

        # Check if the form is valid
        if form.is_valid():
            # Create a new conversation related to the item
            conversation = Conversation.objects.create(item=item)
            
            # Add the logged-in user and the creator of the item as members
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()

            # Save the conversation message, linking it to the newly created conversation
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            # Redirect to the detail view of the item after successful submission
            return redirect('item:detail', pk=item_pk)
    else:
        # If the request method is not POST, initialize an empty form
        form = ConversationMessageForm()
    
    # Render the template for creating a new conversation, passing the form for display
    return render(request, 'conversation/new.html', {'form': form})


@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])

    return render(request, 'conversation/inbox.html', {
        'conversations': conversations
    })


@login_required
def detail(request, pk):
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save()

            return redirect('conversation:detail', pk=pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/detail.html', {
        'conversation': conversation,
        'form': form
    })