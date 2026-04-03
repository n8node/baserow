<template>
  <div class="landing-page">
    <div v-if="pending" class="loading loading--absolute-center" />
    <div v-else-if="error" class="landing-page__error">
      {{ $t('landing.loadError') }}
    </div>
    <template v-else>
      <component
        :is="blockComponent(block.block_type)"
        v-for="block in blocks || []"
        :key="block.id"
        :block="block"
      />
    </template>
  </div>
</template>

<script setup>
import { markRaw } from 'vue'
import LandingService from '@baserow/modules/core/services/landing'
import LandingHero from './blocks/LandingHero'
import LandingFeaturesGrid from './blocks/LandingFeaturesGrid'
import LandingLogos from './blocks/LandingLogos'
import LandingBadges from './blocks/LandingBadges'
import LandingProductTabs from './blocks/LandingProductTabs'
import LandingDeployment from './blocks/LandingDeployment'
import LandingSectionImage from './blocks/LandingSectionImage'
import LandingAutomations from './blocks/LandingAutomations'
import LandingTemplatesGrid from './blocks/LandingTemplatesGrid'
import LandingHowItWorks from './blocks/LandingHowItWorks'
import LandingComparison from './blocks/LandingComparison'
import LandingTestimonials from './blocks/LandingTestimonials'
import LandingCta from './blocks/LandingCta'
import LandingFooter from './blocks/LandingFooter'
import LandingGenericSection from './blocks/LandingGenericSection'

const componentMap = {
  hero: markRaw(LandingHero),
  features_grid: markRaw(LandingFeaturesGrid),
  why_baserow: markRaw(LandingFeaturesGrid),
  logos: markRaw(LandingLogos),
  badges: markRaw(LandingBadges),
  product_tabs: markRaw(LandingProductTabs),
  deployment: markRaw(LandingDeployment),
  ai_assistant: markRaw(LandingSectionImage),
  section_image: markRaw(LandingSectionImage),
  automations: markRaw(LandingAutomations),
  templates_grid: markRaw(LandingTemplatesGrid),
  how_it_works: markRaw(LandingHowItWorks),
  comparison: markRaw(LandingComparison),
  testimonials: markRaw(LandingTestimonials),
  cta: markRaw(LandingCta),
  footer: markRaw(LandingFooter),
  section: markRaw(LandingGenericSection),
}

function blockComponent(type) {
  return componentMap[type] || componentMap.section
}

const { $client } = useNuxtApp()
const { locale } = useI18n()
const i18n = useI18n()
const config = useRuntimeConfig()
const router = useRouter()

const {
  data: blocks,
  pending,
  error,
} = await useAsyncData(
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
      href:
        config.public.publicWebFrontendUrl +
        router.resolve({ name: 'index' }).href,
    },
  ],
})
</script>
