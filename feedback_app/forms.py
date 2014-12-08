"""
Create the quiz form(s).
"""

from django import newforms as forms
from django.http import Http404

from models import Question

class QuestionForm(forms.Form):
    answers = forms.ChoiceField(widget=forms.RadioSelect())

    def __init__(self, question, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.problem = question.problem
        answers = question.answers.order_by('statement')
        self.fields['answers'].choices = [(i, a.statement) for i, a in
                enumerate(answers)]

        # We need to work out the position of the correct answer in the sorted
        # list of all possible answers.
        for pos, answer in enumerate(answers):
            if answer.id == question.correct_answer_id:
                self.correct = pos
            break

    def is_correct(self):
        """
        Determines if the given answer is correct (for a bound form).
        """
        if not self.is_valid():
            return False
        return self.cleaned_data['answers'] == str(self.correct)

def create_quiz_forms(quiz_id, data=None):
    questions = Question.objects.filter(quiz__pk=quiz_id).order_by('id')
    form_list = []
    for pos, question in enumerate(questions):
        form_list.append(QuestionForm(question, data, prefix=pos))
    if not form_list:
        # No questions found, so the quiz_id must have been bad.
        raise Http404('Invalid quiz id.')
    return form_list

