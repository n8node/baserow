<template>
  <section class="landing-hero">
    <div class="landing-hero__container">
      <div v-if="badge" class="landing-hero__badge">
        <span class="landing-hero__badge-dot" />
        {{ badge }}
      </div>
      <h1 class="landing-hero__title">{{ block.title }}</h1>
      <p v-if="block.subtitle" class="landing-hero__subtitle">
        {{ block.subtitle }}
      </p>
      <div class="landing-hero__actions">
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
      <div v-if="selfHostLinks.length" class="landing-hero__self-host">
        {{ selfHostText }}
        <template v-for="(link, i) in selfHostLinks" :key="i">
          <a :href="link.url" class="landing-hero__self-host-link">{{
            link.label
          }}</a>
          <template v-if="i < selfHostLinks.length - 1">, </template>
        </template>
      </div>
      <div v-if="block.image_url" class="landing-hero__image-wrap">
        <img :src="block.image_url" alt="" class="landing-hero__image" />
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import Button from '@baserow/modules/core/components/Button'

const props = defineProps({ block: { type: Object, required: true } })

const extra = computed(() => props.block.extra_data || {})
const badge = computed(() => extra.value.badge || '')
const selfHostLinks = computed(() => extra.value.self_host_links || [])
const selfHostText = computed(
  () => extra.value.self_host_text || 'Prefer to self host?'
)

function ctaProps(url) {
  if (typeof url === 'string' && url.startsWith('/') && !url.startsWith('//')) {
    return { to: url }
  }
  return { tag: 'a', href: url, target: '_blank', rel: 'noopener noreferrer' }
}
</script>
