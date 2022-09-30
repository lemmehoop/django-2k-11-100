from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from web.forms import NoteForm
from web.models import Note, Tag, User


def main_view(request):
    return redirect("notes_list")


def notes_view(request):
    with_alerts = 'with_alerts' in request.GET
    search = request.GET.get("search", None)
    try:
        tag_id = int(request.GET.get("tag_id", None))
    except (TypeError, ValueError):
        tag_id = None

    notes = Note.objects.all().order_by('-created_at')

    if with_alerts:
        notes = notes.filter(alert_send_at__isnull=False)

    if search:
        # title="..." SELECT * FROM web_note WHERE title = "..."
        # title__iexact="..." SELECT * FROM web_note WHERE UPPER(title) = UPPER("...")
        # title__contains="..." SELECT * FROM web_note WHERE title LIKE = "%...%"
        # title__icontains="..." SELECT * FROM web_note WHERE UPPER(title) LIKE = UPPER("%...%")
        notes = notes.filter(
            Q(title__icontains=search) |
            Q(text__icontains=search)
        )

    if tag_id:
        tag = Tag.objects.get(id=tag_id)
        notes = notes.filter(tags__in=[tag])

    return render(request, "web/main.html", {
        'count': Note.objects.count(),
        'notes': notes,
        'with_alerts': with_alerts,
        'query_params': request.GET,
        'search': search,
        'tags': Tag.objects.all(),
        'tag_id': tag_id,
    })


def note_view(request, id):
    note = get_object_or_404(Note, id=id)
    return render(request, "web/note.html", {
        'note': note
    })


def note_edit_view(request, id=None):
    user = User.objects.first()  # TODO get user from auth
    form = NoteForm()
    error, title, text = None, None, None

    note = None
    if id is not None:
        note = get_object_or_404(Note, id=id)
        title = note.title
        text = note.text

    if request.method == 'POST':
        form = NoteForm(request.POST)
        title = request.POST.get("title")
        text = request.POST.get("text")
        print(form.is_valid())
        if form.is_valid():
            if note is None:
                note = Note()
            note.title = title
            note.text = text
            note.user = user
            note.save()
            return redirect('note', note.id)
    return render(request, "web/note_form.html", {
        'title': title,
        'text': text,
        'id': id,
        'form': form
    })
