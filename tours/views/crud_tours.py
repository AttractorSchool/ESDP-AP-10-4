import httpx
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from choices import StatusChoice
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.views.generic.edit import FormMixin
from tours.forms.tour_create_form import TourCreateForm
from tours.models.tour import Tour
from tours.forms.tour_rating_create_form import TourRatingCreateForm

ALLOWED_TO_VIEW = [
    StatusChoice.CONFIRMED,
    StatusChoice.FINISHED,
    StatusChoice.STARTED,
]

ALLOWED_TO_EDIT = [
    StatusChoice.NOT_VERIFIED,
    StatusChoice.SENT_TO_REWORK,
]


class TourListView(ListView):
    model = Tour
    context_object_name = 'tours'
    template_name = 'tour/tour_list.html'

    def get(self, request, *args, **kwargs):
        tours = Tour.objects.all()
        for tour in tours:

            if timezone.now() >= tour.start_date:
                tour.moderation_status = StatusChoice.STARTED

            if timezone.now() >= tour.end_date:
                tour.moderation_status = StatusChoice.FINISHED

            tour.save()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(TourListView, self).get_queryset()
        return queryset.filter(moderation_status='CONFIRMED')


class TourCreateView(CreateView):
    template_name = 'tour/tour_create.html'
    model = Tour
    form_class = TourCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.moderation_status = StatusChoice.SENT_TO_VERIFICATION
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tour_detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_guide \
                    and self.request.user.guide_profile.verification_status == StatusChoice.CONFIRMED:
                return True
        else:
            return False
        return False
@method_decorator(csrf_exempt, name='dispatch')
class TourDetailView(UserPassesTestMixin, FormMixin, DetailView):
    template_name = 'tour/tour_detail.html'
    model = Tour
    context_object_name = 'tour'
    form_class = TourRatingCreateForm

    def get(self, request, pk, *args, **kwargs):
        tour = get_object_or_404(self.model, pk=pk)

        if timezone.now() >= tour.start_date:
            tour.moderation_status = StatusChoice.STARTED

        if timezone.now() >= tour.end_date:
            tour.moderation_status = StatusChoice.FINISHED

        tour.save()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        auth_params = request.POST
        MD = int(auth_params.get('MD'))
        PaRes = auth_params.get('PaRes')

        r = httpx.post(
            'https://api.cloudpayments.ru/payments/cards/post3ds',
            auth=("pk_aad02fa59dec0bacabf00955821fd", "9b431e1c5d36c6c36d01b7635751af5f"),
            json={'TransactionId': MD, 'PaRes': PaRes}
        )
        print(r.json())
        print(args)
        print(kwargs)
        print(request.POST)
        return redirect('tour_detail', pk=kwargs.get("pk"))


    def test_func(self):
        if self.request.user == self.get_object().author:
            return True
        elif self.request.user != self.get_object().author \
                and self.get_object().moderation_status in ALLOWED_TO_VIEW:
            return True
        else:
            return False


class TourUpdateView(UserPassesTestMixin, UpdateView):
    template_name = 'tour/tour_update.html'
    model = Tour
    form_class = TourCreateForm

    def get_success_url(self):
        return reverse('tour_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.moderation_status = StatusChoice.SENT_TO_VERIFICATION
        return super().form_valid(form)

    def test_func(self):
        if self.get_object().author == self.request.user:
            if self.get_object().moderation_status in ALLOWED_TO_EDIT:
                return True
        return False


class TourDeleteView(UserPassesTestMixin, DeleteView):
    model = Tour

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.object.author_id})

    def test_func(self):
        if self.get_object().author == self.request.user \
                and self.get_object().moderation_status == StatusChoice.CONFIRMED:
            return True
        return False
