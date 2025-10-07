from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.utils.timezone import now
from .models import Task

def home(request):
    filter_q = request.GET.get('filter', 'all')
    qs = Task.objects.all().order_by("-created_at")
    if filter_q == 'pending':
        qs = qs.filter(completed=False)
    elif filter_q == 'completed':
        qs = qs.filter(completed=True)
    elif filter_q == 'urgent':
        qs = qs.filter(priority='urgent')
    tasks = qs
    return render(request, "todo/home.html", {"tasks": tasks, "filter": filter_q, "now": now()})

def add_task(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        priority = request.POST.get("priority", "important")
        due_date = request.POST.get("due_date") or None
        if title:
            task = Task.objects.create(title=title, priority=priority, due_date=due_date)
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                html = render_to_string("todo/task_item.html", {"task": task, "now": now()})
                return JsonResponse({"html": html})
        return redirect("home")

def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = not task.completed
    task.save()
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"completed": task.completed})
    return redirect("home")

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"deleted": True})
    return redirect("home")

def undo_delete(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        priority = request.POST.get("priority", "important")
        due_date = request.POST.get("due_date") or None
        if title:
            task = Task.objects.create(title=title, priority=priority, due_date=due_date)
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                html = render_to_string("todo/task_item.html", {"task": task, "now": now()})
                return JsonResponse({"html": html})
    return redirect("home")

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        if title:
            task.title = title
            task.save()
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                html = render_to_string("todo/task_item.html", {"task": task, "now": now()})
                return JsonResponse({"html": html})
    return redirect("home")

def set_priority(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        priority = request.POST.get("priority", task.priority)
        task.priority = priority
        task.save()
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"priority": task.priority})
    return redirect("home")
