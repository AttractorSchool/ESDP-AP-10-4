import httpx
from booking.models import Booking
from choices import StatusChoice, BookingChoice
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.views.generic.edit import FormMixin
from tours.forms.tour_create_form import TourCreateForm
from tours.forms.tour_image_form import TourImageForm
from tours.models.tour import Tour
from tours.models.image import TourImage
from tours.forms.tour_rating_create_form import TourRatingCreateForm
from jobs.jobs import hold_payment_now

from accounts.models import User

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


class TourCreateView(UserPassesTestMixin, CreateView):
    template_name = 'tour/tour_create.html'
    model = Tour
    form_class = TourCreateForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        images = request.FILES.getlist('image')
        if form.is_valid():
            tour = form.save(commit=False)
            tour.author = self.request.user
            tour.moderation_status = StatusChoice.SENT_TO_VERIFICATION
            tour.save()

            for image in images:
                TourImage.objects.create(tour=tour, image=image)

            return redirect(reverse('tour_detail', kwargs={'pk': tour.pk}))
        else:
            return render(request, self.template_name, context={
                'form': form,
                'image_form': TourImageForm(),
            })

    def get(self, request, *args, **kwargs):
        tour_form = TourCreateForm()
        image_form = TourImageForm()
        return render(request, self.template_name, context={
            'form': tour_form,
            'image_form': image_form,
        })

    def test_func(self):
        is_guide = self.request.user.is_guide
        status = self.request.user.guide_profile.verification_status
        if self.request.user.is_authenticated:
            return is_guide and status == StatusChoice.CONFIRMED

        return False


@method_decorator(csrf_exempt, name='dispatch')
class TourDetailView(UserPassesTestMixin, FormMixin, DetailView):
    template_name = 'tour/tour_detail.html'
    model = Tour
    context_object_name = 'tour'
    form_class = TourRatingCreateForm

    def get(self, request, *args, **kwargs):
        tour = get_object_or_404(self.model, pk=kwargs.get('pk'))

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

        response = httpx.post(
            'https://api.cloudpayments.ru/payments/cards/post3ds',
            auth=('pk_aad02fa59dec0bacabf00955821fd', '9b431e1c5d36c6c36d01b7635751af5f'),
            json={'TransactionId': MD, 'PaRes': PaRes},
        )

        response_data = response.json()
        success = response_data['Success']

        token = response_data['Model']['Token']
        account_id = response_data['Model']['AccountId']

        booking = Booking.objects.filter(user_id=account_id, tour_id=kwargs.get('pk')).first()

        if success:
            user = User.objects.filter(pk=account_id).first()
            user.encrypted_card_token = token
            user.save()

            booking.booking_status = BookingChoice.RESERVED
            booking.save()
            httpx.post(
                'https://api.cloudpayments.ru/payments/void',
                auth=('pk_aad02fa59dec0bacabf00955821fd', '9b431e1c5d36c6c36d01b7635751af5f'),
                json={'TransactionId': MD},
            )

            hold_payment_now(booking)

        return redirect('tour_detail', pk=kwargs.get('pk'))

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
