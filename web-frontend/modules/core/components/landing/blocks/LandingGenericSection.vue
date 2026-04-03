<template>
  <section class="landing-generic-section">
    <div class="landing-section-container">
      <div class="landing-generic-section__inner">
        <div
          v-if="block.image_url"
          class="landing-generic-section__image-wrap"
        >
          <img
            class="landing-generic-section__image"
            :src="block.image_url"
            alt=""
          />
        </div>
        <h2
          v-if="block.title"
          class="landing-generic-section__title"
        >
          {{ block.title }}
        </h2>
        <p
          v-if="block.subtitle"
          class="landing-generic-section__subtitle"
        >
          {{ block.subtitle }}
        </p>
        <p
          v-if="block.body"
          class="landing-generic-section__body"
        >
          {{ block.body }}
        </p>
        <div
          v-if="block.primary_cta_label || block.secondary_cta_label"
          class="landing-generic-section__actions"
        >
          <Button
            v-if="block.primary_cta_label && block.primary_cta_url"
            size="large"
            v-bind="ctaProps(block.primary_cta_url)"
          >
            {{ block.primary_cta_label }}
          </Button>
          <Button
            v-if="block.secondary_cta_label && block.secondary_cta_url"
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
import Button from '@baserow/modules/core/components/Button'

defineProps({ block: { type: Object, required: true } })

function ctaProps(url) {
  if (typeof url === 'string' && url.startsWith('/') && !url.startsWith('//')) {
    return { to: url }
  }
  return { tag: 'a', href: url, target: '_blank', rel: 'noopener noreferrer' }
}
</script>
