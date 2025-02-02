# The following file contains in-context-learning prompts for finding bipolarity and depression symptoms.

# Short is the original version from this repository, translated from corean to english and german.

icl_short_en_1 = [
    {
        "role": "system",
        "content": "You'll have several sets of inputs and outputs.\
                    The input is a interview transcript, and the output is a list of Depression and Bipolar symptoms and the section in which they occurred in the previous input.\
                    If you think the patient has Depression and Bipolar symptoms in a given input query, please tell the symptoms and the sections that suggest them.\
                    When answering, please answer symptoms in the form ‘- Symptoms : ...’ and sections in the form ‘- Sections : ...’.\
                    If you don't have Depression and Bipolar symptoms in a given interview, please answer ‘Not applicable’. Do not arbitrarily assume you have Depression or Bipolar symptoms.\
                    Tell us the symptoms and sections only if you are sure.\
                    The symptoms can be answered using in-context learning by referring to the previous set of inputs and outputs.",
    },
    {
        "role": "user",
        "content": "Based on the correspondence and content of the given input and output examples, identify the symptoms of Psychiatric disorders and the sections that suggest them, if any, in the interview shown in the last Input Query. If there are no Depression or Bipolar symptoms in the given interview, answer ‘Not applicable’.",
    },
]

icl_short_de_1 = [
    {
        "role": "system",
        "content": "Sie werden mehrere Sets von Inputs und Outputs haben.\
                    Der Input ist ein Interviewtranskript, und der Output ist eine Liste von Depressions- und bipolaren Symptomen und der Abschnitt, in dem sie im vorherigen Input vorkamen.\
                    Wenn Sie der Meinung sind, dass der Patient in einer bestimmten Input-Query Depressionen und bipolare Symptome aufweist, geben Sie bitte die Symptome und die Abschnitte an, in denen sie vorkommen.\
                    Wenn Sie antworten, geben Sie bitte die Symptome in der Form '- Symptoms : ...' und die Abschnitte in der Form '- Sections:...' an.\
                    Wenn Sie in einem bestimmten Interview keine Depressions- und bipolaren Symptome haben, antworten Sie bitte mit 'Not applicable'. Gehen Sie nicht willkürlich davon aus, dass Sie Depressionen oder bipolare Symptome haben.\
                    Nennen Sie die Symptome und Abschnitte nur wenn Sie sich sicher sind.\
                    Die Symptome können mit Hilfe des in-context-learning beantwortet werden, indem man sich auf den vorherigen Set von Inputs und Outputs bezieht.",
    },
    {
        "role": "user",
        "content": "Identifizieren Sie auf der Grundlage der Übereinstimmungen und des Inhalts der gegebenen Input- und Output-Beispiele die Symptome psychiatrischer Störungen und die Abschnitte, die darauf hindeuten, falls vorhanden, in dem in der letzten Input Query gezeigten Interview. Wenn in dem gegebenen Interview keine Depressions- oder bipolaren Symptome vorhanden sind, antworten Sie ‘Not applicable’.",
    },
]

# Long is the original prompt of the paper in english (see few-shot learning). It has also been translated into german.

icl_long_en_1 = [
    {
        "role": "system",
        "content": "You will be given several sets of inputs and outputs, where the inputs are the interview transcript segments and the outputs are the psychiatric symptoms of associated with Depression and Bipolarity from the previous input and the sections where the symptoms appear.\
            At the end, you will be given a transcript of the interview in Input and asked to identify the psychiatric symptoms associated with Depression and Bipolarity and the section in which the symptom appears, using the form [{‘Symptom’: ‘...’, ‘Section’: ‘...’}, {‘Symptom’: ‘...’, ‘Section’: ‘...’}, ...].\
            If you think there are multiple symptoms in a particular section, you can answer in the form [{‘Symptom’: ‘..., ...’, ‘Section’: ‘...’}, ...].\
            If there are no psychiatric symptoms associated with Depression and Bipolarity in a given interview, answer [{‘Symptom’: ‘none’, ‘Section’: ‘none’}].\
            You can use in-context-learning to answer using the previous input and output sets.\
            I will give you a label(symptom) for a psychiatric symptom associated with Depression and Bipolarity. We have the following 40 symptoms:\
            For Major depression episode: depress(Depressed mood), dinter(Decreased interest),  dapp(Decreased appetite), iapp(Increased appetite), insom(Insomnia), hsom(Hypersomnia), agit(Psychomotor agitation), retard(Psychomotor retardation), fati(Fatigue), worth(Worthlesness), guilty(Excessive guilt), dcon(Decreased concentration), ddeci(Decreased decision), suii(Suicidal ideation), suip(Suicide plan), suia(Suicide attempt), distr(Signficant distress), isoc(Social-occupational impairment), nmed(No medication), npsycho(No pychotic disorder), nbipo(No manic or hypomanic episode).\
            For Bipolar disorder: mood(Expansive mood), iener(increased energy), iself(Increased self-esteem), dsleep(Decreased need for sleep), italk(Increased talk), iidea(Increased ideas), dcon(Decreased concentration), iacti(Increase in goal-directed activity), agit(Psychomotor agitation), irisk(Increased activities with high potential for painful consequences), nmed(No medication) \
            Manic: isoc(Social-occupational impairment), hosp(Hospitalization), psycho(Psychotic features) \
            Hypomanic: change(Change in functioning), obser(Mood disturbance and change in functioning observable by others), nisoc(No social-occupational impairment), nhosp(No hospitalization), npsycho(No psychotic features).\
            When answering a symptom, be sure to answer with a label, and when answering a section, be sure to answer with the exact wording of the interview.",
    },
    {
        "role": "user",
        "content": "Based on the correspondence between the given input and output examples, if you think the interview in the last input has a psychiatric symptom associated with Depression and Bipolarity, provide the symptom and the section that represents it.",
    },
]

icl_long_de_1 = [
    {
        "role": "system",
        "content": "Sie erhalten mehrere Sätze von Inputs und Outputs, wobei die Inputs die Segmente des Interviewtranskripts sind und die Outputs die psychiatrischen Symptome im Zusammenhang mit Depression und Bipolarität aus dem vorherigen Input und die Abschnitte, in denen die Symptome auftreten.\
            Am Ende erhalten Sie ein Transkript des Interviews in Input und werden gebeten, die mit Depression und Bipolarität assoziierten psychiatrischen Symptome und den Abschnitt, in dem das Symptom auftritt, in der Form [{'Symptom': '...', 'Section': '...'}, {'Symptom': '...', 'Section': '...'}, ...] zu identifizieren.\
            Wenn Sie der Meinung sind, dass es in einem bestimmten Abschnitt mehrere Symptome gibt, können Sie in der Form [{'Symptom': '..., ...', 'Section': '...'}, ...] antworten.\
            Wenn in einem bestimmten Interview keine psychiatrischen Symptome im Zusammenhang mit Depressionen und Bipolarität auftreten, antworten Sie mit [{'Symptom': 'none', 'Section': 'none'}].\
            Sie können In-Context-Learning verwenden, um mit den vorherigen Inputs- und Outputssätzen zu antworten.\
            Ich gebe Ihnen ein Label (Symptom) für ein psychiatrisches Symptom, das mit Depression und Bipolarität assoziiert wird. Wir haben die folgenden 40 Symptome:\
            Für eine schwere depressive Episode: depress(Depressive Stimmung), dinter(Vermindertes Interesse), dapp(Verminderter Appetit), iapp(Gesteigerter Appetit), insom(Schlaflosigkeit), hsom(Hypersomnie), agit(Psychomotorische Unruhe), retard(Psychomotorische Retardierung), fati(Müdigkeit), worth(Wertlosigkeit), guilty(Übermäßiges Schuldgefühl), dcon(Verminderte Konzentration), ddeci(Verminderte Entscheidungsfähigkeit), suii(Selbstmordgedanken), suip(Selbstmordpläne), suia(Selbstmordversuch), distr(Signifikante Notlage), isoc(Sozial-berufliche Beeinträchtigung), nmed(Keine Medikamente), npsycho(Keine pychotische Störung), nbipo(Keine manische oder hypomanische Episode) \
            Bei bipolarer Störung: mood(Expansive Stimmung), iener(Gesteigerte Energie), iself(Gesteigertes Selbstwertgefühl), dsleep(Vermindertes Schlafbedürfnis), italk(Gesteigertes Reden), iidea(Gesteigerte Ideen), dcon(Verminderte Konzentration), iacti(Gesteigerte zielgerichtete Aktivität), agit(Psychomotorische Unruhe), irisk(Gesteigerte Aktivitäten mit hohem Potenzial für schmerzhafte Konsequenzen), nmed(Keine Medikation) \
            Manisch: isoc(Sozial-berufliche Beeinträchtigung), hosp(Krankenhausaufenthalt), psycho(Psychotische Merkmale) \
            Hypomanisch: change(Veränderung der Funktionsweise), obser(Stimmungsstörung und Veränderung der Funktionsweise, die von anderen beobachtet werden kann), nisoc(Keine sozial-berufliche Beeinträchtigung), nhosp(Kein Krankenhausaufenthalt), npsycho(Keine psychotischen Merkmale)\
            Achten Sie bei der Beantwortung eines Symptoms darauf, dass Sie mit einer Bezeichnung antworten, und bei der Beantwortung eines Abschnitts darauf, dass Sie den genauen Wortlaut des Interviews wiedergeben.",
    },
    {
        "role": "user",
        "content": "Wenn Sie aufgrund der Übereinstimmung zwischen den gegebenen Inputs- und Outputsbeispielen der Meinung sind, dass das Interview in der letzten Eingabe ein psychiatrisches Symptom aufweist, das mit Depression und Bipolarität in Verbindung steht, geben Sie das Symptom und den Abschnitt an, der es repräsentiert. ",
    },
]
