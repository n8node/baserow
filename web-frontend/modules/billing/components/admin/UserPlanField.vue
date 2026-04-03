<template>
  <div>
    <Badge
      v-if="planName"
      :color="planSlug === 'free' ? 'neutral' : 'cyan'"
      bold
    >
      {{ planName }}
    </Badge>
    <span v-else class="color--neutral">—</span>
  </div>
</template>

<script>
export default {
  name: 'UserPlanField',
  props: {
    row: {
      required: true,
      type: Object,
    },
    column: {
      required: true,
      type: Object,
    },
  },
  computed: {
    planName() {
      return this.row.billing_plan_name || ''
    },
    planSlug() {
      return this.row.billing_plan_slug || ''
    },
  },
}
</script>
