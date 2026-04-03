<template>
  <div class="layout__col-2-scroll layout__col-2-scroll--white-background">
    <div
      style="
        max-width: 600px;
        margin: 80px auto;
        text-align: center;
        padding: 40px 24px;
      "
    >
      <div
        style="
          width: 64px;
          height: 64px;
          border-radius: 50%;
          background: var(--color-success-100);
          display: flex;
          align-items: center;
          justify-content: center;
          margin: 0 auto 24px;
        "
      >
        <i
          class="iconoir-check"
          style="font-size: 32px; color: var(--color-success-600)"
        ></i>
      </div>
      <h1 style="margin-bottom: 8px">
        {{ $t('billing.success.title') }}
      </h1>
      <p style="color: var(--color-neutral-500); margin-bottom: 32px">
        {{ $t('billing.success.description') }}
      </p>
      <div style="display: flex; gap: 12px; justify-content: center">
        <Button @click="goToBilling">
          {{ $t('billing.success.viewSubscription') }}
        </Button>
        <Button type="secondary" @click="goToDashboard">
          {{ $t('billing.success.goToDashboard') }}
        </Button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useNuxtApp } from '#app'
import { useRouter } from 'vue-router'

definePageMeta({
  layout: 'app',
  middleware: 'authenticated',
})

const { $i18n } = useNuxtApp()
useHead({ title: $i18n.t('billing.success.title') })

const router = useRouter()

function goToBilling() {
  router.push({ name: 'billing' })
}

function goToDashboard() {
  router.push({ name: 'dashboard' })
}
</script>
