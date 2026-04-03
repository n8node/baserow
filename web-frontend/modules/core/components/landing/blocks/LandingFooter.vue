<template>
  <footer class="landing-footer">
    <div class="landing-section-container">
      <div class="landing-footer__top">
        <div class="landing-footer__brand">
          <Logo class="landing-footer__logo" />
        </div>
        <div class="landing-footer__columns">
          <div
            v-for="(col, i) in columns"
            :key="i"
            class="landing-footer__col"
          >
            <p class="landing-footer__col-title">{{ col.title }}</p>
            <ul class="landing-footer__col-list">
              <li
                v-for="(link, j) in col.links"
                :key="j"
              >
                <a :href="link.url" class="landing-footer__link">
                  {{ link.label }}
                </a>
              </li>
            </ul>
          </div>
        </div>
        <div v-if="socialLinks.length" class="landing-footer__social">
          <a
            v-for="(s, i) in socialLinks"
            :key="i"
            :href="s.url"
            target="_blank"
            rel="noopener noreferrer"
            class="landing-footer__social-link"
            :title="s.label"
          >
            <span v-html="s.icon_svg || s.label" />
          </a>
        </div>
      </div>
      <div v-if="newsletter" class="landing-footer__newsletter">
        <p class="landing-footer__newsletter-title">
          {{ newsletter.title || 'Join our newsletter' }}
        </p>
        <p
          v-if="newsletter.description"
          class="landing-footer__newsletter-desc"
        >
          {{ newsletter.description }}
        </p>
        <form class="landing-footer__newsletter-form" @submit.prevent>
          <input
            type="email"
            class="landing-footer__newsletter-input"
            :placeholder="newsletter.placeholder || 'Your email address'"
          />
          <button type="submit" class="landing-footer__newsletter-btn">
            {{ newsletter.button || 'Subscribe' }}
          </button>
        </form>
      </div>
      <div class="landing-footer__bottom">
        <p class="landing-footer__copyright">
          {{ copyright }}
        </p>
        <div v-if="legalLinks.length" class="landing-footer__legal">
          <a
            v-for="(l, i) in legalLinks"
            :key="i"
            :href="l.url"
            class="landing-footer__legal-link"
          >
            {{ l.label }}
          </a>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { computed } from 'vue'
import Logo from '@baserow/modules/core/components/Logo'

const props = defineProps({ block: { type: Object, required: true } })
const extra = computed(() => props.block.extra_data || {})
const columns = computed(() => extra.value.columns || [])
const socialLinks = computed(() => extra.value.social_links || [])
const newsletter = computed(() => extra.value.newsletter || null)
const legalLinks = computed(() => extra.value.legal_links || [])
const copyright = computed(
  () =>
    extra.value.copyright ||
    `© ${new Date().getFullYear()} Baserow. All rights reserved.`
)
</script>
