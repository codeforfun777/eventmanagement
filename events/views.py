from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q, Sum
from django.utils import timezone
from .models import Event, Participant, Category
from .forms import EventForm, ParticipantForm, CategoryForm

def dashboard(request):
    today = timezone.now().date()
    
    status_filter = request.GET.get('status', 'today')
    
    total_participants = Participant.objects.count()
    total_events = Event.objects.count()
    upcoming_count = Event.objects.filter(date__gt=today).count()
    past_count = Event.objects.filter(date__lt=today).count()

    events_queryset = Event.objects.select_related('category').prefetch_related('participants')

    if status_filter == 'upcoming':
        display_events = events_queryset.filter(date__gt=today)
        label = "Upcoming Events"
    elif status_filter == 'past':
        display_events = events_queryset.filter(date__lt=today)
        label = "Past Events"
    elif status_filter == 'total':
        display_events = events_queryset.all()
        label = "All Events"
    else:
        display_events = events_queryset.filter(date=today)
        label = "Events Scheduled for Today"    


    search_query = request.GET.get('q')
    if search_query:
        display_events = display_events.filter(
            Q(name__icontains=search_query) | 
            Q(location__icontains=search_query)
        )

    context = {
        'total_participants': total_participants,
        'total_events': total_events,
        'upcoming_count': upcoming_count,
        'past_count': past_count,
        'display_events': display_events,
        'label': label,
    }
    return render(request, 'events_app/dashboard.html', context)


def event_list(request):
    events = Event.objects.select_related('category').prefetch_related('participants').all()
    

    search_query = request.GET.get('q')
    if search_query:
        events = events.filter(
            Q(name__icontains=search_query) | 
            Q(location__icontains=search_query)
        )

  
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        events = events.filter(date__range=[start_date, end_date])

    return render(request, 'events_app/event_list.html', {'events': events})

def manage_event(request, pk=None):
    event = get_object_or_404(Event, pk=pk) if pk else None
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event-list')
    else:
        form = EventForm(instance=event)
    return render(request, 'events_app/event_form.html', {'form': form})


def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event.delete()
    return redirect('event-list')


def manage_category(request, pk=None):
    categories = Category.objects.all()
    

    if pk:
        category = get_object_or_404(Category, pk=pk)
        label = "Update Category"
    else:
        category = None
        label = "Add New Category"

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category-list') 
    else:
        form = CategoryForm(instance=category)
        
    return render(request, 'events_app/category_form.html', {
        'form': form, 
        'categories': categories,
        'label': label
    })

def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category-list')
    return render(request, 'events_app/category_confirm_delete.html', {'category': category})

def register_participant(request):
    selected_event_id = request.GET.get('event_id')

    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        initial_data = {}
        if selected_event_id:
            initial_data['events'] = [selected_event_id]
        
        form = ParticipantForm(initial=initial_data)
    
    return render(request, 'events_app/participant_form.html', {'form': form})