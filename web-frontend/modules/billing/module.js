import {
  defineNuxtModule,
  addPlugin,
  extendPages,
  createResolver,
} from '@nuxt/kit'
import { routes } from './routes'
import { locales } from '../../config/locales.js'

export default defineNuxtModule({
  meta: {
    name: '@baserow/billing',
    configKey: 'billing',
    compatibility: {
      nuxt: '^3.0.0',
    },
  },
  defaults: {},
  hooks: {},
  setup(moduleOptions, nuxt) {
    const { resolve } = createResolver(import.meta.url)

    extendPages((pages) => {
      pages.push(...routes)
    })

    nuxt.hook('i18n:registerModule', (register) => {
      register({
        langDir: resolve('./locales'),
        locales,
      })
    })

    addPlugin(resolve('plugin.js'))
  },
})
