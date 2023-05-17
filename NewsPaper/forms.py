from django.forms import ModelForm
from NewsPaper.news.models import Post
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'category', 'title', 'text']


class BasicSignupForm(SignupForm):
    
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user