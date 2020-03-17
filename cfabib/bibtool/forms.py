from django import forms

from .models import Article

INST_CHOICES = [
    ('HCO','HCO'),
    ('SAO','SAO'),
    ('both','both'),
    ('unknown','unknown'),
    ('neither','neither')
]

class ArticleForm(forms.Form):
	inst = forms.ChoiceField(
			
			choices = forms.CharField(widget=forms.Select(choices=INST_CHOICES))
    )
	class Meta:
		model = Article
		fields = ('inst',) 