from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    # 위젯 설정
    class Meta:
        model = Article
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'placeholder': '제목을 입력하세요'
                }
            )
        }

# class ArticleForm(forms.Form):
#     title = forms.CharField(max_length=140, label='제목',widget=forms.TextInput(
#         attrs={
#             'class':'form-group'
#         }
#     ))
#     content = forms.CharField(label='',widget=forms.Textarea(
#         attrs={
#             'class': 'mx-auto',
#             'placeholder': '내용을 입력하세요',
#             'rows':'30',
#             'width':'50rem',
#         }
#     ))
