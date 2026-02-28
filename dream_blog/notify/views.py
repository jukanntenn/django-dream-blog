from core.views import SetHeadlineMixin
from notifications.views import AllNotificationsList, UnreadNotificationsList


class AllNotificationsListView(SetHeadlineMixin, AllNotificationsList):
    headline = "全部通知"
    paginate_by = 10
    prefetch_related = ("actor", "target")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["num_all"] = self.request.user.notifications.active().count()
        context["num_unread"] = self.request.user.notifications.unread().count()
        # Add elided page range for pagination template
        if context.get("is_paginated"):
            page_obj = context["page_obj"]
            paginator = context["paginator"]
            context["elided_page_range"] = paginator.get_elided_page_range(
                page_obj.number
            )
        return context


class UnreadNotificationsListView(SetHeadlineMixin, UnreadNotificationsList):
    headline = "未读通知"
    paginate_by = 10
    prefetch_related = ("actor", "target")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["num_all"] = self.request.user.notifications.active().count()
        context["num_unread"] = self.request.user.notifications.unread().count()
        # Add elided page range for pagination template
        if context.get("is_paginated"):
            page_obj = context["page_obj"]
            paginator = context["paginator"]
            context["elided_page_range"] = paginator.get_elided_page_range(
                page_obj.number
            )
        return context
