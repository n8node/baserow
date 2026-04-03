<template>
  <section class="landing-templates">
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
      <div class="landing-templates__grid">
        <a
          v-for="(item, i) in items"
          :key="i"
          class="landing-templates__card"
          :href="item.url || '#'"
        >
          <div v-if="item.image" class="landing-templates__card-img-wrap">
            <img
              :src="item.image"
              :alt="item.title || ''"
              class="landing-templates__card-img"
            />
          </div>
          <div class="landing-templates__card-footer">
            <span v-if="item.icon" class="landing-templates__card-icon">
              {{ item.icon }}
            </span>
            <span class="landing-templates__card-title">{{ item.title }}</span>
          </div>
        </a>
      </div>
      <div
        v-if="block.primary_cta_label"
        class="landing-templates__cta"
      >
        <Button
          type="secondary"
          v-bind="ctaProps(block.primary_cta_url)"
        >
          {{ block.primary_cta_label }}
        </Button>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import Button from '@baserow/modules/core/components/Button'

const props = defineProps({ block: { type: Object, required: true } })
const items = computed(() => (props.block.extra_data || {}).items || [])

function ctaProps(url) {
  if (typeof url === 'string' && url.startsWith('/') && !url.startsWith('//')) {
    return { to: url }
  }
  return { tag: 'a', href: url, target: '_blank', rel: 'noopener noreferrer' }
}
</script>
