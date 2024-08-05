from django.contrib import admin

# Let's import the models we created
from .models import SMTPSetting, Campaign, User, Segment, Contact, ContactList, Settings

# Register the models to make them visible on the admin page
admin.site.register(SMTPSetting)
admin.site.register(Settings)
admin.site.register(Campaign)
admin.site.register(User)
admin.site.register(Segment)
admin.site.register(Contact)
admin.site.register(ContactList)
