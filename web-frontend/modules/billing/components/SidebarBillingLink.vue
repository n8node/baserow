<template>
  <li class="context__menu-item">
    <a class="context__menu-item-link" @click="goToBilling">
      <i class="context__menu-item-icon iconoir-credit-card"></i>
      {{ $t('billing.user.menuBilling') }}
    </a>
  </li>
</template>

<script>
export default {
  name: 'SidebarBillingLink',
  methods: {
    goToBilling() {
      this.$emit('hide')
      this.$router.push({ name: 'billing' })
    },
  },
}
</script>
