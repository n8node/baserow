<template>
  <section class="landing-cta" :class="{ 'landing-cta--dark': isDark }">
    <div class="landing-section-container">
      <div class="landing-cta__inner">
        <h2 class="landing-cta__title">{{ block.title }}</h2>
        <p v-if="block.subtitle" class="landing-cta__subtitle">
          {{ block.subtitle }}
        </p>
        <div
          v-if="block.primary_cta_label || block.secondary_cta_label"
          class="landing-cta__actions"
        >
          <Button
            v-if="block.primary_cta_label"
            size="large"
            v-bind="ctaProps(block.primary_cta_url)"
          >
            {{ block.primary_cta_label }}
          </Button>
          <Button
            v-if="block.secondary_cta_label"
            type="secondary"
            size="large"
            v-bind="ctaProps(block.secondary_cta_url)"
          >
            {{ block.secondary_cta_label }}
          </Button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import Button from '@baserow/modules/core/components/Button'

const props = defineProps({ block: { type: Object, required: true } })
const isDark = computed(() => (props.block.extra_data || {}).dark !== false)

function ctaProps(url) {
  if (typeof url === 'string' && url.startsWith('/') && !url.startsWith('//')) {
    return { to: url }
  }
  return { tag: 'a', href: url, target: '_blank', rel: 'noopener noreferrer' }
}
</script>
