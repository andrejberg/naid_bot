

def get_google_location(location):

    u = '<a href="https://www.google.com/maps/search/?api=1&query={}">{}</a>'

    return u.format(location.replace("\n", "").replace(" ", "+"), location)
