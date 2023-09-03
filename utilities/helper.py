from flask import redirect, render_template, session


def login_required(f):
    def check_cookies(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        else:
            return f(*args, **kwargs)
    check_cookies.__name__ = f.__name__
    return check_cookies

def toTime(seconds):
    hours = seconds // 3600
    seconds = seconds % 3600
    minutes = seconds // 60
    seconds = seconds % 60
    return str(hours) + ":"+str(minutes)+":"+str(seconds)


def toSeconds(time):
    holder = []
    try:
        holder = time.split(":")
        if len(holder) == 3:
            total = (int(holder[0]) * 3600) + (int(holder[1]) * 60) + int(holder[2])
        elif len(holder) == 2:
            total = (int(holder[1]) * 60) + int(holder[0])
    except:
        return None
    return int(total)