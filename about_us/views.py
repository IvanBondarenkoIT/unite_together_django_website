from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from unite_together_django_website import settings
from .forms import ContactForm
from .models import History, Mission, Vision, Value, Program, DocumentCategory, Partners
from web_pages.models import BannerSettings

TRY_TO_CREATE_NEW_OBJECTS_IF_NOT_EXIST = True


def get_banner_settings():
    settings, created = BannerSettings.objects.get_or_create(
        id=1
    )  # id=1 для уникальности
    return settings


def first_lunch(request):
    if not History.objects.exists():
        history = History.objects.create(
            content="""
            "Unite Together" була заснована ініціативною групою українців, які прагнули підтримати своїх співвітчизників під час війни. Початок її історії пов'язаний з закупівлею та відправкою необхідних ліків в Україну, зібраних під час благодійних концертів та заходів, аналізом потреб і підтримкою українців, які перебувають у Грузії. З часом організація перетворилася з групи волонтерів, зібраних під час відпустки в Грузії, на структуровану організацію з чітко визначеною місією та стратегією допомоги українцям у Грузії. У червні 2022 року організація провела масштабне опитування серед українців, які проживають у Грузії, що дозволило їй отримати перший грант від європейських партнерів. Крім того, 1 вересня 2022 року Unite Together отримала юридичний статус неприбуткової організації (НГО).
            """
        )
        history.save()
        messages.success(request, "Історія - Імпорт виконано!")

    if not Mission.objects.exists():
        mission = Mission.objects.create(
            content="""
            Наша організація "Unite Together" спрямована на створення та реалізацію проектів, які підтримують і розвивають українців, постраждалих від війни. Наша головна мета — досягти стійких системних змін у їхньому житті та суспільстві.
            """
        )
        mission.save()
        messages.success(request, "Місія - Імпорт виконано!")

    if not Vision.objects.exists():
        vision = Vision.objects.create(
            content="""
            Ми бачимо майбутнє, в якому українці, які пережили трагедію війни, успішно інтегровані в суспільство. Вони мотивовані постійно розвиватися та активно брати участь у формуванні громадянського суспільства та стійких соціальних змін. Наша візія — суспільство, в якому кожна людина має рівні можливості для самореалізації та внеску у добробут суспільства.
            """
        )
        vision.save()
        messages.success(request, "Візія - Імпорт виконано!")

    if not Value.objects.exists():
        value1 = Value.objects.create(
            title="Сталий розвиток і відповідальність",
            content="""
            Ми надаємо велике значення створенню сталих умов для життя і розвитку постраждалих від війни. Ми відповідальні за наші зобов'язання перед бенефіціарами та партнерами.
            """,
        )
        value1.save()
        value2 = Value.objects.create(
            title="Співпраця та партнерство",
            content="""
            Ми цінуємо взаємовигідну та продуктивну співпрацю з нашими партнерами та зацікавленими сторонами. Ми віримо, що тільки завдяки спільним зусиллям ми можемо досягти наших цілей та створити позитивні зміни.
            """,
        )
        value2.save()
        value3 = Value.objects.create(
            title="Співчуття та емпатія",
            content="""
            У нашій роботі ми проявляємо глибоке співчуття та емпатію до всіх, хто потребує нашої підтримки та допомоги. Ми слухаємо і розуміємо потреби наших бенефіціарів, прагнучи надати їм не тільки матеріальну, але й емоційну підтримку.
            """,
        )
        value3.save()
        value4 = Value.objects.create(
            title="Зміни створюються тут",
            content="""
            На початковому етапі діяльності Unite Together організація зосередилася на задоволенні гуманітарних потреб українців у Грузії. Однак з часом цілі організації розширилися, і до гуманітарної місії додалося завдання розвитку та інтеграції українців у грузинське суспільство.
            """,
        )
        value4.save()
        messages.success(request, "Цінності - Імпорт виконано!")

    if not Program.objects.exists():
        program1 = Program.objects.create(
            category="Фінансова підтримка",
            title="#UkrCash програма",
            description="Надано щомісячну фінансову допомогу понад 3000 українцям, на загальну суму більше 2 мільйонів євро цього року.",
            support_partner="ASB",
            beneficiaries_count=3000,
            funding_amount=2000000.00,
        )
        program2 = Program.objects.create(
            category="Підтримка комунальних платежів",
            title="#Програма зимової допомоги",
            description="Покрито комунальні витрати для 670 сімей.",
            support_partner="ASB і PIN",
            beneficiaries_count=670,
        )
        program3 = Program.objects.create(
            category="Підтримка житла",
            title="Підтримка українських громад",
            description="Відшкодування 50% витрат на житло для 90 українських сімей.",
            support_partner="PIN",
            beneficiaries_count=90,
        )
        program4 = Program.objects.create(
            category="Освітні та культурні програми",
            title="Освітні та культурні програми",
            description="Реалізація програм для дітей і літніх людей у Тбілісі, Батумі та Кутаїсі, включаючи освітні заходи, спорт, розваги, мовні курси та майстер-класи.",
        )
        program5 = Program.objects.create(
            category="Спортивні ініціативи",
            title="#UniteForActiveSports програма",
            description="Включає спортивні заходи, такі як скелелазіння, танці, SUP серфінг і кемпінг.",
            support_partner="PIN",
            additional_info="Місця: Тбілісі та Батумі",
        )
        program6 = Program.objects.create(
            category="Підтримка старших людей",
            title="#HandMade програма",
            description="Включає майстер-класи, екскурсії та відвідування культурних заходів, таких як балет.",
            support_partner="CARE",
        )
        program7 = Program.objects.create(
            category="Медичне забезпечення",
            title="Медичне забезпечення",
            description="Надання ліків для лікування захворювань щитовидної залози в Україні та Грузії.",
            beneficiaries_count=1260,
        )
        program1.save()
        program2.save()
        program3.save()
        program4.save()
        program5.save()
        program6.save()
        program7.save()
        messages.success(request, "Програми - Імпорт виконано!")


def who_we_are(request):
    if TRY_TO_CREATE_NEW_OBJECTS_IF_NOT_EXIST:
        first_lunch(request)

    history = History.objects.first()
    mission = Mission.objects.first()
    vision = Vision.objects.first()
    values = Value.objects.all()
    programs = Program.objects.all()
    banner_settings = BannerSettings.objects.first()

    context = {
        "history": history,
        "mission": mission,
        "vision": vision,
        "values": values,
        "programs": programs,
        "banner_settings": banner_settings,
    }

    return render(request, "aboutus/aboutus-index.html", context)


def documents_view(request):
    categories = DocumentCategory.objects.prefetch_related("documents").all()
    banner_settings = BannerSettings.objects.first()
    context = {
        "categories": categories,
        "banner_settings": banner_settings,
    }
    return render(request, "aboutus/about-us-documents.html", context)


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Обробка даних з form.cleaned_data
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            phone_number = form.cleaned_data["phone_number"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]

            # Надсилання електронного листа
            send_mail(
                f"Форма контакту: {subject}",
                f"Ім'я: {first_name} {last_name}\nEmail: {email}\nТелефон: {phone_number}\n\nПовідомлення:\n{message}",
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
            )

            return redirect("contact_success")
    else:
        form = ContactForm()

    banner_settings = BannerSettings.objects.first()

    return render(
        request,
        "aboutus/about-us-contacts.html",
        {"form": form, "banner_settings": banner_settings},
    )


def contact_success_view(request):
    return render(request, "aboutus/contact_success.html")


def about_us(request):
    banner_settings = BannerSettings.objects.first()
    context = {"banner_settings": banner_settings}
    return render(request, "aboutus/aboutus_index.html", context=context)


def history(request):
    banner_settings = BannerSettings.objects.first()
    context = {"banner_settings": banner_settings}
    return render(request, "aboutus/about-us-history.html", context=context)


def documents(request):
    banner_settings = BannerSettings.objects.first()
    context = {"banner_settings": banner_settings}
    return render(request, "aboutus/about-us-documents.html", context=context)


def partners(request):
    partners = Partners.objects.all().order_by("ordering_number")
    banner_settings = BannerSettings.objects.first()
    context = {"partners": partners, "banner_settings": banner_settings}
    return render(request, "aboutus/about-us-partners.html", context=context)


def contacts(request):
    banner_settings = BannerSettings.objects.first()
    context = {"banner_settings": banner_settings}
    return render(request, "aboutus/about-us-contacts.html", context=context)
