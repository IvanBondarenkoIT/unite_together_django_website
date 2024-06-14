from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from unite_together_django_website import settings
from .forms import ContactForm
from .models import History, Mission, Vision, Value, Program, DocumentCategory, Partners

TRY_TO_CREATE_NEW_OBJECTS_IF_NOT_EXIST = True


def first_lunch(request):
    if not History.objects.exists():
        history = History.objects.create(
            content="""
            "Unite Together" was founded by an initiative group of Ukrainians who sought to contribute to supporting their compatriots during the war. The beginning of its history is connected with the purchase and shipment of necessary medicines to Ukraine, collected during charity concerts and events, analysis of the needs and support of Ukrainians who are in Georgia. Over time, the organization has evolved from a group of volunteers gathered during a vacation in Georgia into a structured organization with a clearly defined mission and strategy to help Ukrainians in Georgia. In June 2022, the organization conducted an extensive survey among Ukrainians living in Georgia, which allowed it to receive its first grant from European partners. In addition, on September 1, 2022, Unite Together received legal status as a non-governmental organization (NGO).
            """
        )
        history.save()
        messages.success(request, 'History - Imports done!')

    if not Mission.objects.exists():
        mission = Mission.objects.create(
            content="""
            Our organization "Unite Together" is aimed at creating and implementing projects aimed at supporting and developing Ukrainians affected by the war. Our main goal is to achieve sustainable systemic change in their lives and society.
            """
        )
        mission.save()
        messages.success(request, 'Mission - Imports done!')

    if not Vision.objects.exists():
        vision = Vision.objects.create(
            content="""
            We see a future in which Ukrainians who survived the tragedy of war have successfully integrated into society. They are motivated to constantly develop and actively participate in the formation of civil society and sustainable social change. Our vision is a society in which every person has equal opportunities for self-realization and contribution to the well-being of society.
            """
        )
        vision.save()
        messages.success(request, 'Vision - Imports done!')

    if not Value.objects.exists():
        value1 = Value.objects.create(
            title="Sustainability and responsibility",
            content="""
            We attach great importance to creating sustainable conditions for the life and development of those affected by war. We are responsible for our obligations to beneficiaries and partners.
            """
        )
        value1.save()
        value2 = Value.objects.create(
            title="Cooperation and partnership",
            content="""
            We value mutually beneficial and productive cooperation with our partners and stakeholders. We believe that only through joint efforts can we achieve our goals and create positive change.
            """
        )
        value2.save()
        value3 = Value.objects.create(
            title="Compassion and Empathy",
            content="""
            In our work, we show deep compassion and empathy for everyone who needs our support and help. We listen and understand the needs of our beneficiaries, striving to provide them with not only material but also emotional support.
            """
        )
        value3.save()

        value4 = Value.objects.create(
            title="Changes are created here",
            content="""
            At the initial stage of Unite Together's activities, the organization focused on meeting the humanitarian needs of Ukrainians in Georgia. However, over time, the goals of the organization expanded, and in addition to the humanitarian mission, the task of developing and integrating Ukrainians into Georgian society was added.
            """
        )
        value4.save()
        messages.success(request, 'Value - Imports done!')

    if not Program.objects.exists():
        program1 = Program.objects.create(
            category="Financial support",
            title="#UkrCash program",
            description="Provided monthly financial aid to over 3,000 Ukrainians, totaling more than 2 million euros this year.",
            support_partner="ASB",
            beneficiaries_count=3000,
            funding_amount=2000000.00
        )

        program2 = Program.objects.create(
            category="Utility bills support",
            title="#Winterization program",
            description="Covered utility costs for 670 families.",
            support_partner="ASB and PIN",
            beneficiaries_count=670
        )

        program3 = Program.objects.create(
            category="Housing support",
            title="Support for Ukrainian communities",
            description="Reimbursement of 50% of housing costs for 90 Ukrainian families.",
            support_partner="PIN",
            beneficiaries_count=90
        )

        program4 = Program.objects.create(
            category="Educational and cultural programs",
            title="Educational and cultural programs",
            description="Implementation of programs for children and the elderly in Tbilisi, Batumi, and Kutaisi, including educational events, sports, entertainment, language lessons, and master classes."
        )

        program5 = Program.objects.create(
            category="Sports initiatives",
            title="#UniteForActiveSports program",
            description="Includes sports activities like rock climbing, dancing, SUP surfing, and camping.",
            support_partner="PIN",
            additional_info="Locations: Tbilisi and Batumi"
        )

        program6 = Program.objects.create(
            category="Support for older people",
            title="#HandMade program",
            description="Includes workshops, excursions and visits to cultural events such as ballet.",
            support_partner="CARE"
        )

        program7 = Program.objects.create(
            category="Medical provision",
            title="Medical provision",
            description="Provision of drugs for the treatment of thyroid diseases in Ukraine and Georgia.",
            beneficiaries_count=1260
        )
        program1.save()
        program2.save()
        program3.save()
        program4.save()
        program5.save()
        program6.save()
        program7.save()
        messages.success(request, 'Program - Imports done!')


def who_we_are(request):
    if TRY_TO_CREATE_NEW_OBJECTS_IF_NOT_EXIST:
        first_lunch(request)

    history = History.objects.first()
    mission = Mission.objects.first()
    vision = Vision.objects.first()
    values = Value.objects.all()
    programs = Program.objects.all()

    context = {
        'history': history,
        'mission': mission,
        'vision': vision,
        'values': values,
        'programs': programs,
    }

    return render(request, 'aboutus/about-us-history.html', context)


def documents_view(request):
    categories = DocumentCategory.objects.prefetch_related('documents').all()
    context = {
        'categories': categories,
    }
    return render(request, 'aboutus/about-us-documents.html', context)


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the data in form.cleaned_data
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Send email (for example)
            send_mail(
                f'Contact Form: {subject}',
                f'Name: {first_name} {last_name}\nEmail: {email}\nPhone: {phone_number}\n\nMessage:\n{message}',
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],  # Ensure you have this setting
            )

            return redirect('contact_success')
    else:
        form = ContactForm()

    return render(request, 'aboutus/contact.html', {'form': form})


def contact_success_view(request):
    return render(request, 'aboutus/contact_success.html')


def about_us(request):
    context = {}
    return render(request, 'aboutus/aboutus_index.html', context=context)


def history(request):
    context = {}
    return render(request, 'aboutus/about-us-history.html', context=context)


def documents(request):
    context = {}
    return render(request, 'aboutus/about-us-documents.html', context=context)


def partners(request):
    partners = Partners.objects.all()
    return render(request, 'aboutus/about-us-partners.html', {'partners': partners})


# def partners(request):
#     context = {}
#     return render(request, 'aboutus/about-us-partners.html', context=context)


def contacts(request):
    context = {}
    return render(request, 'aboutus/about-us-contacts.html')