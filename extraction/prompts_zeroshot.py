# The following file contains zero-shoot prompts for finding bipolarity and depression symptoms.

# Short is the original version from this repository, translated from corean to english and german.

zeroshot_short_en_1 = [
    {
        "role": "system",
        "content": "You will be given the following interview between a psychiatrist and a patient. If you think there are any psychiatrically significant symptoms in the following interview, please tell what they are and the sections that suggest them.\
                    Please answer symptoms in the form '- Symptoms : ...' and sections in the form '- Sections : ...'.\
                    If there are no psychiatrically significant symptoms in a given interview, please answer 'N/A'.\
                    Psychiatrically significant symptoms are the following 40 symptoms:\
                    For Major depression episode: depress(Depressed mood), dinter(Decreased interest),  dapp(Decreased appetite), iapp(Increased appetite), insom(Insomnia), hsom(Hypersomnia), agit(Psychomotor agitation), retard(Psychomotor retardation), fati(Fatigue), worth(Worthlesness), guilty(Excessive guilt), dcon(Decreased concentration), ddeci(Decreased decision), suii(Suicidal ideation), suip(Suicide plan), suia(Suicide attempt), distr(Signficant distress), isoc(Social-occupational impairment), nmed(No medication), npsycho(No pychotic disorder), nbipo(No manic or hypomanic episode) \
                    For Bipolar disorder: mood(Expansive mood), iener(increased energy), iself(Increased self-esteem), dsleep(Decreased need for sleep), italk(Increased talk), iidea(Increased ideas), dcon(Decreased concentration), iacti(Increase in goal-directed activity), agit(Psychomotor agitation), irisk(Increased activities with high potential for painful consequences), nmed(No medication) \
                    Manic: isoc(Social-occupational impairment), hosp(Hospitalization), psycho(Psychotic features) \
                    Hypomanic: change(Change in functioning), obser(Mood disturbance and change in functioning observable by others), nisoc(No social-occupational impairment), nhosp(No hospitalization), npsycho(No psychotic features) \
                    ",
    },
    {
        "role": "user",
        "content": "If you think the following consultation has psychiatrically significant symptoms, please tell what they are and the sections in the text where you find these symptoms.",
    },
]

zeroshot_short_de_1 = [
    {
        "role": "system",
        "content": "Ihnen wird das folgende Gespräch zwischen einem Psychiater und einem Patienten vorgelegt. Wenn Sie der Meinung sind, dass in dem folgenden Gespräch psychiatrisch bedeutsame Symptome vorkommen, geben Sie bitte an, um welche Symptome es sich handelt und welche Abschnitte darauf hindeuten.\
                    Bitte beantworten Sie Symptome in der Form '- Symptoms : ...' und Abschnitte in der Form '- Sections : ...'.\
                    Wenn es in einem bestimmten Interview keine psychiatrisch bedeutsamen Symptome gibt, antworten Sie bitte mit 'N/A'.\
                    Psychiatrisch bedeutsame Symptome sind die folgenden 40 Symptome:\
                    Für eine schwere depressive Episode: depress(Depressive Stimmung), dinter(Vermindertes Interesse), dapp(Verminderter Appetit), iapp(Gesteigerter Appetit), insom(Schlaflosigkeit), hsom(Hypersomnie), agit(Psychomotorische Unruhe), retard(Psychomotorische Retardierung), fati(Müdigkeit), worth(Wertlosigkeit), guilty(Übermäßiges Schuldgefühl), dcon(Verminderte Konzentration), ddeci(Verminderte Entscheidungsfähigkeit), suii(Selbstmordgedanken), suip(Selbstmordpläne), suia(Selbstmordversuch), distr(Signifikante Notlage), isoc(Sozial-berufliche Beeinträchtigung), nmed(Keine Medikamente), npsycho(Keine pychotische Störung), nbipo(Keine manische oder hypomanische Episode) \
                    Bei bipolarer Störung: mood(Expansive Stimmung), iener(Gesteigerte Energie), iself(Gesteigertes Selbstwertgefühl), dsleep(Vermindertes Schlafbedürfnis), italk(Gesteigertes Reden), iidea(Gesteigerte Ideen), dcon(Verminderte Konzentration), iacti(Gesteigerte zielgerichtete Aktivität), agit(Psychomotorische Unruhe), irisk(Gesteigerte Aktivitäten mit hohem Potenzial für schmerzhafte Konsequenzen), nmed(Keine Medikation) \
                    Manisch: isoc(Sozial-berufliche Beeinträchtigung), hosp(Krankenhausaufenthalt), psycho(Psychotische Merkmale) \
                    Hypomanisch: change(Veränderung der Funktionsweise), obser(Stimmungsstörung und Veränderung der Funktionsweise, die von anderen beobachtet werden kann), nisoc(Keine sozial-berufliche Beeinträchtigung), nhosp(Kein Krankenhausaufenthalt), npsycho(Keine psychotischen Merkmale)\
                    ",
    },
    {
        "role": "user",
        "content": "Wenn Sie der Meinung sind, dass die folgende Befragung psychiatrisch bedeutsame Symptome aufweist, geben Sie bitte an, um welche Symptome es sich handelt und in welchen Abschnitten des Textes Sie diese Symptome finden.",
    },
]

# Long is the original prompt of the paper in english. It has also been translated into german.
zeroshot_long_en_1 = [
    {
        "role": "system",
        "content": "You will be given an interview. When answering the psychiatric symptoms associated with Bipolarity or Depression and the section that represents them, please be sure to answer in the form [{‘Symptom’: ‘...’, ‘Section’: ‘...’}, {‘Symptom’: ‘...’, ‘Section’: ‘...’}, ...].\
                   If you think there are multiple symptoms in a particular section, you can answer in the form [{‘Symptom’: ‘..., ...’, ‘Section’: ‘...’}, ...].\
                   If there are no psychiatric symptoms associated with Bipolarity and Depression in a given interview, please answer [{‘Symptom’: ‘none’, ‘Section’: ‘none’}].\
                   We will give you a label (symptom) for the psychiatric symptoms associated with Bipolarity and Depression. We have the following 40 symptoms:\
                   For Major depression episode: depress(Depressed mood), dinter(Decreased interest),  dapp(Decreased appetite), iapp(Increased appetite), insom(Insomnia), hsom(Hypersomnia), agit(Psychomotor agitation), retard(Psychomotor retardation), fati(Fatigue), worth(Worthlesness), guilty(Excessive guilt), dcon(Decreased concentration), ddeci(Decreased decision), suii(Suicidal ideation), suip(Suicide plan), suia(Suicide attempt), distr(Signficant distress), isoc(Social-occupational impairment), nmed(No medication), npsycho(No pychotic disorder), nbipo(No manic or hypomanic episode) \
                   For Bipolar disorder: mood(Expansive mood), iener(increased energy), iself(Increased self-esteem), dsleep(Decreased need for sleep), italk(Increased talk), iidea(Increased ideas), dcon(Decreased concentration), iacti(Increase in goal-directed activity), agit(Psychomotor agitation), irisk(Increased activities with high potential for painful consequences), nmed(No medication) \
                   Manic: isoc(Social-occupational impairment), hosp(Hospitalization), psycho(Psychotic features).\
                   Hypomanic: change(Change in functioning), obser(Mood disturbance and change in functioning observable by others), nisoc(No social-occupational impairment), nhosp(No hospitalization), npsycho(No psychotic features).\
                   When answering a symptom, be sure to use a label, and when answering a section, be sure to use the exact words from the interview.",
    },
    {
        "role": "user",
        "content": "Look at the following interview and if you think that there are psychiatric symptoms associated with Bipolarity and Depression in the interview, please tell me the symptom and the section that represents it",
    },
]

zeroshot_long_de_1 = [
    {
        "role": "system",
        "content": "Sie werden ein Interview erhalten. Achten Sie bei der Beantwortung der psychiatrischen Symptome im Zusammenhang mit Bipolarität oder Depression und dem entsprechenden Abschnitt darauf, in der Form [{'Symptom': '...', 'Section': '...'}, {'Symptom': '...', 'Section': '...'}, ...] zu antworten.\
                   Wenn Sie der Meinung sind, dass es in einem bestimmten Abschnitt mehrere Symptome gibt, können Sie in der Form [{'Symptom': '..., ...', 'Section': '...'}, ...] antworten.\
                   Wenn in einem bestimmten Interview keine psychiatrischen Symptome im Zusammenhang mit Bipolarität und Depression auftreten, antworten Sie bitte in der Form [{'Symptom': 'none', 'Section': 'none'}].\
                   Wir geben Ihnen eine Bezeichnung (Symptom) für die psychiatrischen Symptome im Zusammenhang mit Bipolarität und Depression. Wir haben die folgenden 40 Symptome:\
                   Für eine  depressive Episode: depress(Depressive Stimmung), dinter(Vermindertes Interesse), dapp(Verminderter Appetit), iapp(Gesteigerter Appetit), insom(Schlaflosigkeit), hsom(Hypersomnie), agit(Psychomotorische Unruhe), retard(Psychomotorische Retardierung), fati(Müdigkeit), worth(Wertlosigkeit), guilty(Übermäßiges Schuldgefühl), dcon(Verminderte Konzentration), ddeci(Verminderte Entscheidungsfähigkeit), suii(Selbstmordgedanken), suip(Selbstmordpläne), suia(Selbstmordversuch), distr(Signifikante Notlage), isoc(Sozial-berufliche Beeinträchtigung), nmed(Keine Medikamente), npsycho(Keine pychotische Störung), nbipo(Keine manische oder hypomanische Episode) \
                   Bei bipolarer Störung: mood(Expansive Stimmung), iener(Gesteigerte Energie), iself(Gesteigertes Selbstwertgefühl), dsleep(Vermindertes Schlafbedürfnis), italk(Gesteigertes Reden), iidea(Gesteigerte Ideen), dcon(Verminderte Konzentration), iacti(Gesteigerte zielgerichtete Aktivität), agit(Psychomotorische Unruhe), irisk(Gesteigerte Aktivitäten mit hohem Potenzial für schmerzhafte Konsequenzen), nmed(Keine Medikation) \
                   Manisch: isoc(Sozial-berufliche Beeinträchtigung), hosp(Krankenhausaufenthalt), psycho(Psychotische Merkmale) \
                   Hypomanisch: change(Veränderung der Funktionsweise), obser(Stimmungsstörung und Veränderung der Funktionsweise, die von anderen beobachtet werden kann), nisoc(Keine sozial-berufliche Beeinträchtigung), nhosp(Kein Krankenhausaufenthalt), npsycho(Keine psychotischen Merkmale)\
                   Achten Sie bei der Beantwortung eines Symptoms darauf, dass Sie eine Bezeichnung verwenden, und bei der Beantwortung eines Abschnitts darauf, dass Sie den genauen Wortlaut des Interviews verwenden.",
    },
    {
        "role": "user",
        "content": "Schauen Sie sich das folgende Interview an, und wenn Sie der Meinung sind, dass es psychiatrische Symptome gibt, die mit Bipolarität und Depression in Verbindung stehen, nennen Sie mir bitte das Symptom und den Abschnitt, der es darstellt",
    },
]
