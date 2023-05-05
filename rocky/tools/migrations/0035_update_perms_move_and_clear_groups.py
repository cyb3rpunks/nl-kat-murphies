# Generated by Django 3.2.18 on 2023-04-26 13:54

from django.contrib.auth import get_user_model
from django.db import migrations

from tools.models import OrganizationMember

User = get_user_model()


def add_group_permissions(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    try:
        admin = Group.objects.get(name="admin")
        admin.permissions.add(Permission.objects.get(codename="add_indemnification"))
    except Group.DoesNotExist:
        pass


def migrate_user_groups_to_organizationmember(apps, schema_editor):
    members = OrganizationMember.objects.all()
    for member in members:
        user_groups = member.user.groups.all()
        member.groups.add(*user_groups)


def clear_group_from_users(apps, schema_editor):
    users = User.objects.all()
    for user in users:
        user.groups.clear()


class Migration(migrations.Migration):
    dependencies = [("tools", "0034_organizationmember_groups")]

    operations = [
        migrations.RunPython(add_group_permissions),
        migrations.RunPython(migrate_user_groups_to_organizationmember),
        migrations.RunPython(clear_group_from_users),
    ]