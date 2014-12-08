from django.forms import ModelForm
from django.shortcuts import render_to_response, get_object_or_404
from kwippyproject.kwippy.models.page_setting import PageSetting

class Page_SettingForm(ModelForm):
    class Meta:
        model = PageSetting
        exclude = ('user',)
    def save(self, request):
        page_settings = get_object_or_404(PageSetting, user=int(request.user.id))
        page_settings.save()
        return page_settings
