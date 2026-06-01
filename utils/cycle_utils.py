from datetime import datetime, timedelta


def get_cycle_info(period_dates, cycle_length=28, period_length=5):
    """
    period_dates: ['2026-01-10', '2026-02-07', ...]
    cycle_length: kullanıcının ortalama döngü uzunluğu
    period_length: kanama süresi
    """

    if not period_dates:
        return {
            "current_cycle_day": 1,
            "cycle_length": cycle_length,
            "period_length": period_length,
            "next_period_date": "N/A",
            "days_until_next_period": 0,
            "is_period_expected": False
        }

    # Tarihleri sırala
    sorted_dates = sorted(
        datetime.strptime(d, "%Y-%m-%d").date()
        for d in period_dates
    )

    last_period_start = sorted_dates[-1]
    today = datetime.today().date()

    # Bugün ile son regl başlangıcı arasındaki gün
    days_since_last_period = (today - last_period_start).days

    # Döngü günü
    current_cycle_day = (days_since_last_period % cycle_length) + 1

    # Sonraki regl tahmini
    next_period_date = last_period_start + timedelta(days=cycle_length)

    # Eğer tarih geçmişte kaldıysa ileri taşı
    while next_period_date <= today:
        next_period_date += timedelta(days=cycle_length)

    # Kaç gün kaldı
    days_until_next_period = (next_period_date - today).days

    # Regl yakın mı?
    is_period_expected = days_until_next_period <= 3

    return {
        "current_cycle_day": current_cycle_day,
        "cycle_length": cycle_length,
        "period_length": period_length,
        "next_period_date": next_period_date.strftime("%Y-%m-%d"),
        "days_until_next_period": days_until_next_period,
        "is_period_expected": is_period_expected
    }