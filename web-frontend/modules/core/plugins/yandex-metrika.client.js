import { nextTick } from 'vue'
import { useNuxtApp, useRouter, useRuntimeConfig } from '#imports'

/**
 * Yandex.Metrika for the Nuxt SPA: init + virtual pageviews on client-side navigations.
 * Counter ID from runtimeConfig.public.yandexMetrikaId (NUXT_PUBLIC_YANDEX_METRIKA_ID).
 */
export default defineNuxtPlugin(() => {
  const router = useRouter()
  const runtimeConfig = useRuntimeConfig()
  const nuxtApp = useNuxtApp()

  const idRaw = runtimeConfig.public.yandexMetrikaId
  const counterId =
    typeof idRaw === 'number' ? idRaw : Number.parseInt(String(idRaw || ''), 10)

  if (!import.meta.client || !Number.isFinite(counterId) || counterId <= 0) {
    return
  }

  window.dataLayer = window.dataLayer || []

  const tagUrl = `https://mc.yandex.ru/metrika/tag.js?id=${counterId}`

  // Official loader (avoids duplicate script tags)
  ;(function (m, e, t, r, i, k, a) {
    m[i] =
      m[i] ||
      function () {
        ;(m[i].a = m[i].a || []).push(arguments)
      }
    m[i].l = 1 * new Date()
    for (let j = 0; j < document.scripts.length; j++) {
      if (document.scripts[j].src === r) {
        return
      }
    }
    k = e.createElement(t)
    a = e.getElementsByTagName(t)[0]
    k.async = 1
    k.src = r
    a.parentNode.insertBefore(k, a)
  })(window, document, 'script', tagUrl, 'ym')

  window.ym(counterId, 'init', {
    ssr: true,
    webvisor: true,
    clickmap: true,
    ecommerce: 'dataLayer',
    referrer: document.referrer,
    url: location.href,
    accurateTrackBounce: true,
    trackLinks: true,
  })

  let firstAfterEach = true

  router.afterEach((to) => {
    nextTick(() => {
      // Initial load is covered by ym init(); avoid double-counting the first pageview.
      if (firstAfterEach) {
        firstAfterEach = false
        return
      }

      if (to.meta.preventPageViewTracking) {
        return
      }

      const url = `${window.location.origin}${to.fullPath}`
      window.ym(counterId, 'hit', url)
    })
  })

  nuxtApp.provide('yandexMetrika', {
    counterId,
    hit: (url) => window.ym(counterId, 'hit', url),
  })
})
