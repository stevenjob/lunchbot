import datetime

from PS4Config import DEFAULT_MAX_PLAYERS, PLAY_TIME

punctuation = [".", "?", ","]
time_prefixes = ["at"]
competitive_keywords = ["compet", "competitive", "1v1", "1v1me"]

def today_at(hour, min):
    return datetime.datetime.today().replace(
                    hour = hour,
                    minute = min,
                    second = 0,
                    microsecond = 0)

def parse_time(s):
    am_pm = ""
    if len(s) >= 3 and s[-1] == "m" and (s[-2] == "a" or s[-2] == "p"):
        am_pm = s[-2]
        s = s[:-2]

    time_parts = s.split(":")
    if len(time_parts) > 2:
        raise ValueError

    if len(time_parts) == 1:
        time_parts = s.split(".")

    if len(time_parts) == 1:
        time_parts.append("00")
    elif len(time_parts[1]) != 2:
        raise ValueError

    hour = int(time_parts[0])
    min = int(time_parts[1])

    if hour < 0 or min < 0:
        raise ValueError

    if len(am_pm):
        if hour > 12:
            raise ValueError
        if am_pm == "p":
            hour += 12
    else:
        # no am/pm specified, if it's before 8:00, assume they mean afternoon
        if hour < 8:
            hour += 12

    return today_at(hour, min)

def maybe_parse_time(s):
    try:
        return parse_time(s)
    except ValueError:
        return None

def pretty_mode(mode):
    if mode == "compet":
        return "Competitive"
    return mode

def parse_game_initiation(str):
    parts = str.split(" ")

    when = None
    desc_parts = []
    player_count = DEFAULT_MAX_PLAYERS
    mode = None
    play_time = PLAY_TIME
    for part in parts:
        while len(part) and part[-1] in punctuation:
            part = part[:-1]

        maybe_when = maybe_parse_time(part)
        if maybe_when:
            if when:
                return None

            when = maybe_when
            if len(desc_parts) and desc_parts[-1] in time_prefixes:
                desc_parts.pop()
            continue

        if part == "sextuple":
            player_count = 6
            continue
        if part in competitive_keywords:
            player_count = 2
            mode = "compet"
            play_time = 20
            continue

        desc_parts.append(part)

    if not when:
        return None

    return when, " ".join(desc_parts), player_count, play_time, mode
