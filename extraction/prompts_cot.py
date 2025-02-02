# The following file contains chain-of-thought prompts for finding bipolarity and depression symptoms.

# Short is the original version from this repository, translated from corean to english and german.

cot_short_en_1 = (
    {
        "role": "system",
        "content": "You'll be given a set of example Inputs and Outputs.\
        The Input is the interview transcript, and the Output describes the specific Depression and Bipolar symptoms found in that section based on the definition of Depression and Bipolar symptoms given in the previous Input.\
        When answering, please refer to the input and output forms given above. If there are multiple symptoms in a section, you can answer multiple times.\
        If you think there are multiple Depression and Bipolar symptoms in a given Input Query, you can answer multiple symptoms and sections.\
        If you don't have Depresion and Bipolar symptoms in a given interview, answer ‘Not applicable’.",
    },
    {
        "role": "user",
        "content": "Based on the correspondence and content of the given input and output examples, if the patient in the last Input Query shows Depression and Bipolar symptoms, please tell the symptoms and the sections that suggest them.",
    },
)

cot_short_de_1 = (
    {
        "role": "system",
        "content": "Sie erhalten eine Reihe von Inputs und Outputs als Beispiele.\
        Der Input ist das Interviewtranskript, und der Output beschreibt die spezifischen Depressions- und bipolaren Symptome, die in diesem Abschnitt gefunden wurden, basierend auf der Definition der Depressions- und bipolaren Symptome, die im vorherigen Input gegeben wurde.\
        Beziehen Sie sich bei der Beantwortung bitte auf die oben angegebenen Inputs- und Outputsformulare. Wenn es in einem Abschnitt mehrere Symptome gibt, können Sie mehrfach antworten.\
        Wenn Sie der Meinung sind, dass es mehrere Depressions- und bipolare Symptome in einer bestimmten Input Query gibt, können Sie mehrere Symptome und Abschnitte beantworten.\
        Wenn Sie in einer bestimmten Befragung keine Depressions- und bipolaren Symptome haben, antworten Sie mit „Not applicable“.",
    },
    {
        "role": "user",
        "content": "Wenn der Patient in der letzten Input Query Depressionen und bipolare Symptome aufweist, geben Sie bitte auf der Grundlage der angegebenen Inputs- und Outputsbeispiele die Symptome und die Abschnitte an, die darauf hindeuten. ",
    },
)


# There is no original prompt for chain-of-thoughts in the paper ("long" version).
