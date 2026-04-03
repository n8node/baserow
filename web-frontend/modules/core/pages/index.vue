<template>
  <LandingPage />
</template>

<script setup>
import LandingPage from '@baserow/modules/core/components/landing/LandingPage'

definePageMeta({
  name: 'index',
  layout: 'landing',
  middleware: ['settings'],
  /** Used by global `authentication` middleware to skip /login on stale refresh token */
  publicGuestHome: true,
})

const store = useNuxtApp().$store
if (store.getters['auth/isAuthenticated']) {
  await navigateTo({ name: 'dashboard' })
}
</script>
