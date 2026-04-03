/**
 * Gates in-app notifications UI (sidebar bell, unread dots). Store, API, and
 * realtime handlers stay active so the feature can be re-enabled later via
 * BASEROW_NOTIFICATIONS_UI_VISIBLE / NUXT_PUBLIC_BASEROW_NOTIFICATIONS_UI_VISIBLE.
 */
export default {
  computed: {
    notificationsUiVisible() {
      const v = this.$config.public.baserowNotificationsUiVisible
      return v === true || v === 'true'
    },
  },
}
