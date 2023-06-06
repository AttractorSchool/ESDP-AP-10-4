from accounts.models import GuideProfile


def create_user(form):
    user = form.save(commit=False)
    user.set_password(form.cleaned_data.get('password'))
    user.save()
    return user


def create_profile(user):
    if user.is_guide:
        GuideProfile.objects.get_or_create(user=user)
        user.guide_profile.save()
