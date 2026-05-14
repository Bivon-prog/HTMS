"""Mission-local and HQ-Nairobi working-hour SLA deadlines (SRS 4.1, pdf2)."""
from __future__ import annotations

from datetime import datetime, time, timedelta
from typing import TYPE_CHECKING

import pytz
from django.utils import timezone

if TYPE_CHECKING:
    from apps.missions.models import Mission


def _is_hq_nairobi_working(dt_utc: datetime) -> bool:
    loc = dt_utc.astimezone(pytz.timezone('Africa/Nairobi'))
    if loc.weekday() >= 5:
        return False
    t = loc.time()
    return time(8, 0) <= t <= time(17, 0)


def add_working_hours_calendar(
    start_utc: datetime,
    hours_to_add: float,
    is_working,
    *,
    max_calendar_days: int = 400,
) -> datetime:
    """Advance ``start_utc`` by ``hours_to_add`` hours counted only when ``is_working(dt)`` is true."""
    if hours_to_add <= 0:
        return start_utc
    remaining_seconds = hours_to_add * 3600.0
    current = start_utc
    step = timedelta(minutes=1)
    cap = 60 * 24 * max_calendar_days
    for _ in range(cap):
        if remaining_seconds <= 0:
            return current
        if is_working(current):
            remaining_seconds -= 60.0
        current += step
    return current


def add_mission_working_hours(mission: Mission, start_utc: datetime, hours_to_add: float) -> datetime:
    return add_working_hours_calendar(
        start_utc,
        hours_to_add,
        lambda dt: mission.is_working_hours(dt),
    )


def add_hq_nairobi_working_hours(start_utc: datetime, hours_to_add: float) -> datetime:
    return add_working_hours_calendar(start_utc, hours_to_add, _is_hq_nairobi_working)


def compute_ticket_sla_due(ticket) -> datetime | None:
    """Return SLA due instant in UTC from now, based on escalation tier (pdf2)."""
    from apps.missions.models import TicketCategory

    cat: TicketCategory = ticket.category
    hours = cat.auto_escalation_hours
    if not hours:
        return None
    now = timezone.now()
    if ticket.escalated_to_hq:
        return add_hq_nairobi_working_hours(now, float(hours))
    return add_mission_working_hours(ticket.mission, now, float(hours))


def recalculate_ticket_sla(ticket, *, from_time: datetime | None = None) -> None:
    from django.utils import timezone as dj_tz

    cat = ticket.category
    hours = cat.auto_escalation_hours
    if not hours:
        ticket.sla_due_date = None
        return
    base = from_time or dj_tz.now()
    if ticket.escalated_to_hq:
        ticket.sla_due_date = add_hq_nairobi_working_hours(base, float(hours))
    else:
        ticket.sla_due_date = add_mission_working_hours(ticket.mission, base, float(hours))
