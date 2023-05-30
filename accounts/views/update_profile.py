# from choices import StatusChoice
# from django.contrib.auth.mixins import UserPassesTestMixin
# from django.urls import reverse_lazy
# from django.views.generic import UpdateView
#
# from accounts.forms import ProfileUpdateForm
# from accounts.models import Profile
#
# ALLOWED_TO_EDIT = [
#     StatusChoice.NOT_VERIFIED,
#     StatusChoice.SENT_TO_REWORK,
#     StatusChoice.CONFIRMED,
# ]
#
#
# class UpdateGuideProfile(UserPassesTestMixin, UpdateView):
#     model = Profile
#     form_class = ProfileUpdateForm
#     template_name = 'update_profile.html'
#     context_object_name = 'form'
#     success_url = reverse_lazy('login')
#
#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         self.object.verification_status = StatusChoice.SENT_TO_VERIFICATION
#         form = self.get_form()
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)
#
#     def test_func(self):
#         if self.request.user == self.get_object().user:
#             if self.get_object().verification_status in ALLOWED_TO_EDIT:
#                 return True
#             else:
#                 return False
#         else:
#
#             return False
