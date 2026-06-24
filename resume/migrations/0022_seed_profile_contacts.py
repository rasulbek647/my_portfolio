from django.db import migrations


def seed_profile_contacts(apps, schema_editor):
    ResumeProfile = apps.get_model('resume', 'ResumeProfile')
    profile, created = ResumeProfile.objects.get_or_create(pk=1)
    
    # Contact info
    if not profile.email:
        profile.email = 'boyjonovanasiba518@gmail.com'
    if not profile.phone:
        profile.phone = '+998905795559'
    if not profile.telegram:
        profile.telegram = 'https://t.me/matyoquboff_01'
    if not profile.instagram:
        profile.instagram = '@matyoquboff___'
    if not profile.location:
        profile.location = 'Xiva'
    if not profile.location_uz:
        profile.location_uz = 'Xiva'
    if not profile.location_en:
        profile.location_en = 'Khiva'
    if not profile.location_ru:
        profile.location_ru = 'Хива'

    # Name info
    if not profile.full_name:
        profile.full_name = 'Matyoqubov Rasulbek'
    if not profile.full_name_uz:
        profile.full_name_uz = 'Matyoqubov Rasulbek'
    if not profile.full_name_en:
        profile.full_name_en = 'Matyoqubov Rasulbek'
    if not profile.full_name_ru:
        profile.full_name_ru = 'Матякубов Расулбек'

    profile.save()


def reverse_seed(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0021_add_hero_greeting_fields'),
    ]

    operations = [
        migrations.RunPython(seed_profile_contacts, reverse_seed),
    ]
