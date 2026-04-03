<template>
  <section
    class="landing-section-image"
    :class="{
      'landing-section-image--reversed': reversed,
      'landing-section-image--gray': grayBg,
    }"
  >
    <div class="landing-section-container">
      <div class="landing-section-header">
        <div class="landing-section-header__line" />
        <h2 v-if="block.title" class="landing-section-header__title">
          {{ block.title }}
        </h2>
        <p v-if="block.subtitle" class="landing-section-header__subtitle">
          {{ block.subtitle }}
        </p>
      </div>
      <div class="landing-section-image__layout">
        <div v-if="sidebarItems.length" class="landing-section-image__sidebar">
          <div
            v-for="(item, i) in sidebarItems"
            :key="i"
            class="landing-section-image__sidebar-item"
          >
            <span
              v-if="item.icon"
              class="landing-section-image__sidebar-icon"
            >
              {{ item.icon }}
            </span>
            {{ item.label }}
          </div>
        </div>
        <div v-if="block.image_url" class="landing-section-image__img-wrap">
          <img
            :src="block.image_url"
            alt=""
            class="landing-section-image__img"
          />
        </div>
      </div>
      <div v-if="block.body" class="landing-section-image__body">
        {{ block.body }}
      </div>
      <div
        v-if="block.primary_cta_label || block.secondary_cta_label"
        class="landing-section-image__actions"
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
  </section>
</template>

<script setup>
import { computed } from 'vue'
import Button from '@baserow/modules/core/components/Button'

const props = defineProps({ block: { type: Object, required: true } })
const extra = computed(() => props.block.extra_data || {})
const reversed = computed(() => !!extra.value.reversed)
const grayBg = computed(() => !!extra.value.gray_background)
const sidebarItems = computed(() => extra.value.sidebar || [])

function ctaProps(url) {
  if (typeof url === 'string' && url.startsWith('/') && !url.startsWith('//')) {
    return { to: url }
  }
  return { tag: 'a', href: url, target: '_blank', rel: 'noopener noreferrer' }
}
</script>
