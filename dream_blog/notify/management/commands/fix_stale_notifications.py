from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from notifications.models import Notification


class Command(BaseCommand):
    help = "Fix stale ContentType references in notifications after comment model migration"

    def handle(self, *args, **options):
        # Get old and new ContentTypes
        old_ct = ContentType.objects.filter(
            app_label="tree_comments", model="treecomment"
        ).first()

        from comments.models import Comment

        new_ct = ContentType.objects.get_for_model(Comment)

        if not old_ct:
            self.stdout.write(
                self.style.WARNING("No stale ContentType found. Nothing to do.")
            )
            return

        # Find affected notifications
        affected = Notification.objects.filter(target_content_type=old_ct)
        count = affected.count()

        if count == 0:
            self.stdout.write(self.style.WARNING("No affected notifications found."))
            return

        self.stdout.write(f"Found {count} notifications with stale ContentType.")

        # Update the ContentType for all affected notifications
        updated = affected.update(target_content_type=new_ct)

        self.stdout.write(
            self.style.SUCCESS(f"Successfully updated {updated} notifications.")
        )

        # Verify the fix
        remaining = Notification.objects.filter(target_content_type=old_ct).count()
        if remaining == 0:
            self.stdout.write(self.style.SUCCESS("All stale references fixed."))
        else:
            self.stdout.write(
                self.style.ERROR(f"Failed to fix {remaining} notifications.")
            )
