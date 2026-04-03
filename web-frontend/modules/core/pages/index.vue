<template>
  <LandingPage />
</template>

<script setup>
import LandingPage from '@baserow/modules/core/components/landing/LandingPage'

definePageMeta({
  name: 'index',
  layout: 'landing',
  middleware: ['settings'],
})

const store = useNuxtApp().$store
if (store.getters['auth/isAuthenticated']) {
  await navigateTo({ name: 'dashboard' })
}
</script>
