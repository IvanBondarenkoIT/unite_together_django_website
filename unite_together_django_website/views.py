from django.shortcuts import render


def privacy_policy(request):
    return render(request, "includes/terms_conditions_politics/privacy_policy.html")


def terms_conditions(request):
    return render(request, "includes/terms_conditions_politics/terms_conditions.html")


def cookies_policy(request):
    return render(request, "includes/terms_conditions_politics/cookies_policy.html")
