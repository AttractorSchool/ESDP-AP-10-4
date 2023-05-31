from accounts.models import GuideProfile


def create_profile(form):
    user = form.save()
    user.set_password(form.cleaned_data.get('password'))
    if form.cleaned_data.get("is_guide"):
        GuideProfile.objects.create(user=user)
        user.guide_profile.save()
        return user
    return user
