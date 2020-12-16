from covid.models import Covid, Reservation
from django.shortcuts import render
from datetime import datetime, timedelta


# alog_view est le nom de ma vue qui sera utilisisée dans urls.py
def algo_view(request):

    today = datetime.now()
    stats = []  # ici je met tout dans la même list et ne fait pas zip() mais c'est pariel

    # Exemple de contenu attendu dans stats lorsqu'il sera rempli
    # stats = [
    #   (today,1,2,0,1),
    #   (yesterday,1,1,0,1),
    #   (2days ago,0,0,0,1),
    #   (3days ago,0,0,1,1),
    #   ...
    # ]
    #  /!\ ici je met today, yesterday, ... mais c'est des datetime

    for i in range(0, 30):
        date = today - timedelta(days=i)
        stats_for_the_date = (
            date,
            covid_positive_at(date),
            covid_positive_30_days_before(date),
            covid_contact_at(date),
            covid_contact_30_days_before(date),
        )
        stats.append(stats_for_the_date)

    # le commentaire suivant est mis ici mais concerne la template

    # Dans la template a chaque tour de boucle for il prend une ligne de stats
    # Exemple premier tour de boucle:
    # for date, covid_that_day, covid_30_days, covid_contacts_that_day, covid_contacts_30_days in stats:
    #     print(date)  --> today
    #     print(covid_that_day) --> 1
    #     print(covid_30_days) --> 2
    #     print(covid_contacts_that_day) --> 0
    #     print(covid_contacts_30_days) --> 1

    templates_values = {"stats": stats}
    return render(request, "algo.html", templates_values)


###########################################################################################################################################


def covid_positive_at(date):
    return covid_positive_within(start_date=date, end_date=date)


def covid_positive_30_days_before(date):
    return covid_positive_within(start_date=date - timedelta(days=30), end_date=date)


def covid_positive_within(start_date, end_date):
    """
    Fonction dont le but est de rechercher le nombre de test covid effectué durant la periode qui commence à start_date et fini à end_date
    """

    covids = Covid.objects.filter(test_date__gte=start_date, test_date__lte=end_date)
    return len(covids)


###########################################################################################################################################


def covid_contact_at(date):
    return covid_contact_within(start_date=date, end_date=date)


def covid_contact_30_days_before(date):
    return covid_contact_within(start_date=date - timedelta(days=30), end_date=date)


def covid_contact_within(start_date, end_date):
    """
    Fonction dont le but est de rechercher le nombre de contact fait avec des personnes qui ont été testées positives durant la periode
    qui commence à start_date et fini à end_date

    Une personne est considérée contagieuse 5jours autour de son test
        -> Les personnes potentielement contagieuse à une certaine date sont donc les personnes prise dans l'intervalle [date-4 ; date+4]
        -> Dans notre cas elles sont prise dans l'intervalle [start_date-4 ; end_date+4]

        Exemple de ligne du temps dans lequel on recherche les tests positifs:
            - start_date = J6
            - end_date = J9
        |-J1-|-J2-|-J3-|-J4-|-J5-|-J6-|-J7-|-J8-|-J9-|-J10|-J11|-J12|-J13|-J14|-J15|-J16|
        |----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
        |----|-XX-|-XX-|-XX-|-XX-|-XX-|-XX-|-XX-|-XX-|-XX-|-XX-|-XX-|-XX-|----|----|----|
        |----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|

    """

    covids = Covid.objects.filter(
        test_date__gte=start_date - timedelta(days=4), test_date__lte=end_date + timedelta(days=4)
    )

    users_who_have_been_tested_positive = []
    reservations_for_positive_users_within_range = []

    for covid in covids:
        # one user with covid
        user_who_have_been_tested_positive = covid.user

        # add this user to a list that contains all users with covid
        users_who_have_been_tested_positive.append(user_who_have_been_tested_positive)

        # get all reservation for this user
        reservations_for_a_positive_user_within_range = Reservation.objects.filter(
            user=user_who_have_been_tested_positive
        ).filter(date__gte=start_date, date__lte=end_date)

        # add user's reservations to a list that contains all reservations for all users with covid
        reservations_for_positive_users_within_range.extend(reservations_for_a_positive_user_within_range)

    reservations_without_covid_with_contact = []

    for reservation in reservations_for_positive_users_within_range:
        # get user's reservations at the same place at the same date that a covid user reservation for users without covid
        reservations_without_covid_same_place_same_date = (
            Reservation.objects.filter(establishment=reservation.establishment)
            .filter(date=reservation.date)
            .exclude(user__in=users_who_have_been_tested_positive)
        )
        reservations_without_covid_with_contact.extend(reservations_without_covid_same_place_same_date)

    # Take care of values that may have been added twice or more
    # set(a_list) remove doubles in a_list
    unique_reservations_without_covid_with_contact = set(reservations_without_covid_with_contact)

    # return number -> len()
    return len(unique_reservations_without_covid_with_contact)