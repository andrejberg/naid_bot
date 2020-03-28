"""
NAid Bot

Text templates for communication with user.
"""

# ------------------ COMMAND REPLY --------------------------------------------
template_help_message = """\
<b>Alle:</b>
/help Zeigt diese Nachricht

<b>Hinweise:</b>
/uebergabe
/bezahlung
/handschuhe
/maske
... weitere Punkte folgen

<b>Gruppenmitglieder:</b>
/auftrag Einen Auftrag aufgeben
/delete Einen Aftrag loeschen (noch nicht implementiert)

<b>for beta phase:</b>
/test Post a demo task
"""


template_start_not_authorized = """\
<em>Tut mir leid, ich kenne dich noch nicht gut genug. Bitte schreibe \
mir das erste mal ueber die Gruppe damit ich weiss, dass du berechtigt bist \
mir Aufgaben zu erteilen.</em>
"""

template_cant_init_conversation = """\
<em>Tut mir leid {first_name}, ich kann dir noch nicht antworten. Bitte \
starte eine private Konversation mit mir: @naid_demo_bot</em>
"""

template_error_not_text = """\
<em>Bitte verwende nur Text.</em>
"""

template_error_unknown = """\
<em>Irgendwas ist schief gegangen.</em>
"""

# ----------------- HINWEISE ----------------------------
template_help_uebergabe = """\
<b>Uebergabe</b>
<em>Vermeide bitte den direkten Kontakt so weit wie moeglich. Stelle die \
Einkaeufe vor die Haustuer. Weite Infos folgen....</em>
"""

template_help_bezahlung = """\
<b>Bezahlung</b>
<em>Natuerlich ist die Sache hier ehrenamtlich. Trotzdem muss das Geld \
fuers Einkaufen etc. uebergeben werden. Weite Infos folgen....</em>
"""

template_help_handschuhe = """\
<b>Handschuhe</b>
<em>Handschuhe (Latex) helfen vielleicht dabei hygienischer zu arbeiten \
sie ersetzen allgemeine Regeln aber nicht wie: Nicht ins Gesicht fassen. \
Weite Infos folgen....
Denke bitte auch daran, dass Handschuhe, wie sie im Krankenhaus benutzt werden, \
derzeit dringen gebraucht werden....</em>
"""

template_help_maske = """\
<b>Maske</b>
<em>Eine Gesichtsmaske (Stoff, Cellulose) ist ein guter Weg andere \
vor einer Troepfcheninfektion durch dich zu schuetzen. Aber ... \
Weite Infos folgen....
Denke bitte auch daran, dass Masken, wie sie im Krankenhaus benutzt werden, \
derzeit dringen gebraucht werden....</em>
"""

# ---------------- FOR RECORD OF TASK -------------------
template_record_title = """\
<em>Gib zuerst eine allgeine Beschreibung wobei Hilfe benoetigt \
wird. Dieser Text wird oeffentlich angezeigt, deswegen bitte \
keine persoenlichen Informationen.</em>
"""

template_record_description = """\
<em>Gib nun eine genauere Beschreibung. Diese Informationen \
werden erst nach einer Bestaetigung durch dich weitergegeben. \
Die Adresse kannst du im naechsten Stritt eingeben.</em>
"""

template_record_location = """\
<em>Gib nun ein Adresse oder einen Ort ein.</em>
"""

# ---------------- FOR CLIENT ---------------------------
# show client overview of task after recording
template_task_client_overview = """\
<b>Oeffentlich in der Gruppe sichtbar:</b>
{title}

<b>Nur nach Bestaetigung im privaten Chat sichtbar:</b>
{description}


{location}

"""

# show client to confirm
template_task_client_confirm = """\
<em><a href='tg://user?id={volunteer_user_id}'>{volunteer_first_name}</a> \
hat sich dazu bereit erklaert folgende Aufgabe zu uebernehmen:</em>

{title}

<em>Bitte bestaetige, dass du diesen Auftrag an {volunteer_first_name} vergeben moechtest. \
Im Anschluss werden die Details und der Ort uebermittelt.</em>
"""

# show client after conformation while volunteer has not confirmed yet
template_task_client_confirmed_wait = """
<em>Danke, fuer das Vertrauen in {volunteer_first_name}. Warte auf Bestaetigung \
durch {volunteer_first_name}... </em>
"""

# show client after both have confirmed
template_task_client_confirmed_both = """
<em>{volunteer_first_name} hat bestaetigt und wird die Aufgabe erledigen. \

Bitte bestaetige, dass alles erledigt ist, wenn es soweit ist.</em>
"""

# show client after volunteer has declined
template_task_client_declined_by_volunteer = """\
<em>{volunteer_first_name} hat es sich anderst ueberlegt und ist zurueck getreten. \
Die Aufgabe wurde wieder in der Gruppe freigegeben.</em>
"""

template_task_client_done = """\
<b>Auftrag:</b>

{title}

<em>Wurde von {volunteer_first_name} erledigt.</em>
"""
# -------------------------------------------------------

# ---------------- FOR GROUP --------------------------
# show in group (DO NOT SHOW PRIVATE INFORMATION!!!)
template_task_group_open = """\
<em><a href='tg://user?id={client_user_id}'>{client_first_name}</a> hat \
folgende Aufgabe gepostet:</em>

{title}

<em>Wer moechte helfen?</em>
"""

# show in group while task not finished yet
template_task_group_processing = """\
<em><a href='tg://user?id={client_user_id}'>{client_first_name}</a> hat \
folgende Aufgabe gepostet:</em>

{title}

<em>Wird von {volunteer_first_name} erledigt...</em>
"""

# show in group as soon as task is finished
template_task_group_done = """\
<em><a href='tg://user?id={client_user_id}'>{client_first_name}</a> hat \
folgende Aufgabe gepostet:</em>

{title}

<em>Wurde erledigt. Vielen Dank {volunteer_first_name}!</em>
"""
# -------------------------------------------------------

# ------------- FOR VOLUNTEER --------------------------
# show volunteer for conformation
template_task_volunteer_confirm = """\
<em>Hi {volunteer_first_name}! Du hast dich dazu bereit erklaert folgende Aufgabe \
zu uebernehmen:</em>

{title}

<em>Bitte bestaetige, dass du wirlich bereit bist du helfen. Im Anschluss werden dir\
persoenliche Daten uebermittelt.</em>
"""

# show volunteer after conformation while waiting for clients conformation
template_task_volunteer_confirmed_wait = """\
<em>Danke fuer dein Engagement! Bitte gedulde dich noch etwas bis \
<a href='tg://user?id={client_user_id}'>{client_first_name}</a> \
die Freigabe erteilt...</em>
"""

# show volunteer after both have confirmed
template_task_volunteer_confirmed_both = """\
<em>Es kann los gehen. Hier sind die weiteren Details. Bitte denke daran, dass es \
sich um persoenliche Daten handelt und gehe vertraulich damit um.</em>

{title}

{description}

{location}

<em>Falls du noch fragen hast melde dich bitte bei \
<a href='tg://user?id={client_user_id}'>{client_first_name}</a>. \
Ich kann dir auch Hinweise geben. Schreibe mir dazu einfach '/help' um \
mehr zu erfahren. Viel Erfolg.

Bitte bestaetige wenn Alles erledigt ist.</em>
"""

# show volunteer after client has declined
template_task_volunteer_declined_by_client = """\
<em>Tut mir leid. {client_first_name} moechte die Aufgabe nicht an dich vergeben. \
Die Aufgabe wurde wieder freigegeben. Bitte versuche es mit einer anderen \
Aufgabe.</em>
"""

template_task_volunteer_done = """\
Danke {volunteer_first_name}! Weiter so.
"""
# -------------------------------------------------------
