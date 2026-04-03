<template>
  <Badge
    v-if="planName && planSlug !== 'free'"
    v-tooltip="$t('billing.badge.tooltip', { plan: planName })"
    :color="badgeColor"
    bold
  >
    {{ planName }}
  </Badge>
</template>

<script>
export default {
  name: 'SubscriptionBadge',
  computed: {
    subscriptionData() {
      return (
        this.$store.getters['auth/getAdditionalUserData']?.subscription || null
      )
    },
    planName() {
      return this.subscriptionData?.plan_name || ''
    },
    planSlug() {
      return this.subscriptionData?.plan_slug || 'free'
    },
    badgeColor() {
      const colors = {
        free: 'neutral',
        starter: 'cyan',
        business: 'yellow',
        enterprise: 'purple',
        premium: 'cyan',
      }
      return colors[this.planSlug] || 'cyan'
    },
  },
}
</script>
