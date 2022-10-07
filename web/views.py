from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, RedirectView, FormView, CreateView

from web.forms import NoteForm, AuthForm
from web.models import Note, Tag, User


class NotesListView(ListView):
    template_name = 'web/main.html'

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Note.objects.none()
        queryset = Note.objects.filter(user=self.request.user).order_by('-created_at')
        return self.filter_queryset(queryset)

    def filter_queryset(self, notes):
        self.with_alerts = 'with_alerts' in self.request.GET
        self.search = self.request.GET.get("search", None)
        try:
            self.tag_id = int(self.request.GET.get("tag_id", None))
        except (TypeError, ValueError):
            self.tag_id = None

        if self.with_alerts:
            notes = notes.filter(alert_send_at__isnull=False)

        if self.search:
            # title="..." SELECT * FROM web_note WHERE title = "..."
            # title__iexact="..." SELECT * FROM web_note WHERE UPPER(title) = UPPER("...")
            # title__contains="..." SELECT * FROM web_note WHERE title LIKE = "%...%"
            # title__icontains="..." SELECT * FROM web_note WHERE UPPER(title) LIKE = UPPER("%...%")
            notes = notes.filter(
                Q(title__icontains=self.search) |
                Q(text__icontains=self.search)
            )

        if self.tag_id:
            tag = Tag.objects.get(id=self.tag_id)
            notes = notes.filter(tags__in=[tag])
        return notes

    def get_context_data(self, *, object_list=None, **kwargs):
        if not self.request.user.is_authenticated:
            return {}
        return {
            **super(NotesListView, self).get_context_data(),
            'count': Note.objects.filter(user=self.request.user).count(),
            'with_alerts': self.with_alerts,
            'search': self.search,
            'tag_id': self.tag_id,
            'query_params': self.request.GET,
            'tags': Tag.objects.filter(user=self.request.user),
        }


class NoteDetailView(DetailView):
    template_name = 'web/note.html'
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)


class NoteCreateFormView(CreateView):
    form_class = NoteForm
    template_name = 'web/note_form.html'

    def get_initial(self):
        return {'user': self.request.user}

    def get_success_url(self):
        return reverse('note', args=(self.object.title, self.object.id))


@login_required
def note_edit_view(request, id=None, title=None):
    form = NoteForm()

    note = None
    if id is not None:
        note = get_object_or_404(Note, user=request.user, id=id)
        form = NoteForm(instance=note)

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note, initial={'user': request.user})
        if form.is_valid():
            note = form.save()
            return redirect('note', note.title, note.id)

    return render(request, "web/note_form.html", {
        'id': id,
        'form': form,
        'title': getattr(note, 'title')
    })


class RegistrationView(View):
    def _render(self, request, form=None, is_success=False):
        return render(request, "web/registration.html", {
            "form": form or AuthForm(),
            'is_success': is_success
        })

    def get(self, request, *args, **kwargs):
        return self._render(request)

    def post(self, request, *args, **kwargs):
        is_success = False
        form = AuthForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            is_success = True
        return self._render(request, form, is_success)


def login_view(request):
    form = AuthForm()
    message = None
    if request.method == 'POST':
        form = AuthForm(request.POST)
        if form.is_valid():
            user = authenticate(request, **form.cleaned_data)
            if user is None:
                message = "Электронная почта или пароль неправильные"
            else:
                login(request, user)
                next_url = 'main'
                if 'next' in request.GET:
                    next_url = request.GET.get("next")
                return redirect(next_url)
    return render(request, "web/login.html", {
        "form": form,
        'message': message
    })


def logout_view(request):
    logout(request)
    return redirect('main')
