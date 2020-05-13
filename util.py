import datetime


def existingsnippet_monday(today):
    """Return a datetime.date object: the monday for existing snippets.

    The rule is that we show the snippets for the previous week.  We
    declare a week starts on Monday...well, actually, Sunday at 11pm.
    The reason for this is that (for quota reasons) we sent out a
    reminder email Sunday at 11:50pm rather than Monday morning, and
    we want that to count as 'Monday' anyway...

    Arguments:
       today: the current day as a datetime.datetime object, used to
          calculate the best monday.

    Returns:
       The Monday that we are accepting new snippets for, by default,
       as a datetime.date (not datetime.datetime) object.
    """
    today_weekday = today.weekday()   # monday == 0, sunday == 6
    if today_weekday == 6 and today.hour >= 23:
        end_monday = today - datetime.timedelta(today_weekday)
    else:
        end_monday = today - datetime.timedelta(today_weekday + 7)
    return end_monday.date()
