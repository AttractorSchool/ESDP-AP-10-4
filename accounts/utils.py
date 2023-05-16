from accounts.models import Profile


def create_profile(form):
    user = form.save()
    user.set_password(form.cleaned_data.get('password'))
    Profile.objects.create(user=user)
    if form.cleaned_data.get('is_guide') is None:
        user.profile.is_guide = False
        user.profile.save()
        return user
    user.profile.is_guide = form.cleaned_data.get('is_guide')
    user.profile.save()
    return user


