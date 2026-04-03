<template>
  <div class="landing-page">
    <div v-if="pending" class="loading loading--absolute-center" />
    <div v-else-if="error" class="landing-page__error">
      {{ $t('landing.loadError') }}
    </div>
    <template v-else>
      <section
        v-for="block in blocks || []"
        :key="block.id"
        class="landing-page__block"
        :class="`landing-page__block--${block.block_type}`"
      >
        <div
          v-if="block.image_url"
          class="landing-page__block-image-wrap"
        >
          <img
            class="landing-page__block-image"
            :src="block.image_url"
            alt=""
          />
        </div>
        <div class="landing-page__block-inner">
          <h1
            v-if="block.block_type === 'hero' && block.title"
            class="landing-page__title landing-page__title--hero"
          >
            {{ block.title }}
          </h1>
          <h2
            v-else-if="block.title"
            class="landing-page__title"
          >
            {{ block.title }}
          </h2>
          <p
            v-if="block.subtitle"
            class="landing-page__subtitle"
          >
            {{ block.subtitle }}
          </p>
          <p
            v-if="block.body"
            class="landing-page__body"
          >
            {{ block.body }}
          </p>
          <div
            v-if="
              block.primary_cta_label ||
                block.secondary_cta_label
            "
            class="landing-page__actions"
          >
            <Button
              v-if="block.primary_cta_label && block.primary_cta_url"
              size="large"
              v-bind="ctaLinkProps(block.primary_cta_url)"
            >
              {{ block.primary_cta_label }}
            </Button>
            <Button
              v-if="block.secondary_cta_label && block.secondary_cta_url"
              type="secondary"
              size="large"
              v-bind="ctaLinkProps(block.secondary_cta_url)"
            >
              {{ block.secondary_cta_label }}
            </Button>
          </div>
        </div>
      </section>
    </template>
  </div>
</template>

<script setup>
import Button from '@baserow/modules/core/components/Button'
import LandingService from '@baserow/modules/core/services/landing'

const { $client } = useNuxtApp()
const { locale } = useI18n()
const i18n = useI18n()
const config = useRuntimeConfig()
const router = useRouter()

const { data: blocks, pending, error } = await useAsyncData(
  'landing-home-blocks',
  async () => {
    const loc = locale.value === 'en' ? 'en' : 'ru'
    const { data } = await LandingService($client).fetchBlocks(loc)
    return data
  },
  { watch: [locale] }
)

useHead({
  title: i18n.t('landing.metaTitle'),
  bodyAttrs: { class: 'landing-body' },
  link: [
    {
      rel: 'canonical',
      href: config.public.publicWebFrontendUrl + router.resolve({ name: 'index' }).href,
    },
  ],
})

function isInternalPath(url) {
  return (
    typeof url === 'string' &&
    url.startsWith('/') &&
    !url.startsWith('//')
  )
}

function ctaLinkProps(url) {
  if (isInternalPath(url)) {
    return { to: url }
  }
  return {
    tag: 'a',
    href: url,
    target: '_blank',
    rel: 'noopener noreferrer',
  }
}
</script>
