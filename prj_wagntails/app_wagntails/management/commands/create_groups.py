import logging

from django.contrib.auth.models import User, Group, Permission
from django.core.management import BaseCommand

GROUPS = {
    "Administration": {
        # general permissions
        "log entry": ["add", "delete", "change", "view"],
        "group": ["add", "delete", "change", "view"],
        "permission": ["add", "delete", "change", "view"],
        "user": ["add", "delete", "change", "view"],
        "content type": ["add", "delete", "change", "view"],
        "session": ["add", "delete", "change", "view"],

        # django app model specific permissions
        "customer": ["add", "delete", "change", "view"],
        "order": ["add", "delete", "change", "view"],
        "product": ["add", "delete", "change", "view"],
        "tag": ["add", "delete", "change", "view"],
    },

    "customer": {
        # django app model specific permissions
        "customer": ["view"],
        "order": ["add", "delete", "change", "view"],
        "product": ["add", "delete", "change", "view"],
        "tag": ["add", "delete", "change", "view"],
    },

    "owner": {
        # django app model specific permissions
        "customer": ["view"],
        "dog": ["add", "delete", "change", "view"],
        "volunteer": ["view"],
        "tag": ["add", "delete", "change", "view"],
    },

    "volunteer": {
        # django app model specific permissions
        "customer": ["view"],
        "owner": ["view"],
        "dog": ["view"],
        "tag": ["add", "delete", "change", "view"],
    },
}

USERS = {
    "Admin": ["Administration", "sreeku.ralla@gmail.com", "Sri1@kam"],
}


class Command(BaseCommand):
    help = "Creates read only default permission groups for users"

    def handle(self, *args, **options):

        for group_name in GROUPS:

            new_group, created = Group.objects.get_or_create(name=group_name)

            # Loop models in group
            for app_model in GROUPS[group_name]:

                # Loop permissions in group/model
                for permission_name in GROUPS[group_name][app_model]:

                    # Generate permission name as Django would generate it
                    name = "Can {} {}".format(permission_name, app_model)
                    print("Creating {}".format(name))

                    try:
                        model_add_perm = Permission.objects.get(name=name)
                    except Permission.DoesNotExist:
                        logging.warning("Permission not found with name '{}'.".format(name))
                        continue

                    new_group.permissions.add(model_add_perm)

            for user_name in USERS:

                new_user = None
                if user_name == "Admin":
                    new_user, created = User.objects.get_or_create(username=user_name, is_staff=True, is_superuser=True,
                                                                   email=USERS[user_name][1])
                else:
                    new_user, created = User.objects.get_or_create(username=user_name, is_staff=True,
                                                                   email=USERS[user_name][1])

                new_user.set_password(USERS[user_name][2])
                new_user.save()

                if USERS[user_name][0] == str(new_group):
                    new_group.user_set.add(new_user)

                    print("Adding {} to {}".format(user_name, new_group))
