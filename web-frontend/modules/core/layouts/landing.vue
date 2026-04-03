<template>
  <div class="landing-layout">
    <Toasts />
    <header class="landing-layout__header">
      <NuxtLink :to="{ name: 'index' }" class="landing-layout__logo">
        <Logo />
      </NuxtLink>
      <div class="landing-layout__header-actions">
        <LangPicker />
        <Button type="secondary" size="small" :to="{ name: 'login' }">
          {{ $t('landing.logIn') }}
        </Button>
        <Button
          v-if="settings.allow_new_signups"
          size="small"
          :to="{ name: 'signup' }"
        >
          {{ $t('landing.signUp') }}
        </Button>
      </div>
    </header>
    <main class="landing-layout__main">
      <slot />
    </main>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

import Toasts from '@baserow/modules/core/components/toasts/Toasts'
import Logo from '@baserow/modules/core/components/Logo'
import LangPicker from '@baserow/modules/core/components/LangPicker'
import Button from '@baserow/modules/core/components/Button'

export default {
  name: 'LandingLayout',
  components: { Toasts, Logo, LangPicker, Button },
  computed: {
    ...mapGetters({
      settings: 'settings/get',
    }),
  },
}
</script>
