import { BillingPlugin } from '@baserow/modules/billing/plugins'
import {
  BillingProvidersAdminType,
  BillingPlansAdminType,
} from '@baserow/modules/billing/adminTypes'
import { BillingMembersPagePluginType } from '@baserow/modules/billing/membersPagePluginTypes'
import billingStore from '@baserow/modules/billing/store/billing'

export default defineNuxtPlugin({
  name: 'billing',
  dependsOn: ['core', 'client-handler'],
  setup(nuxtApp) {
    const { $registry, $store } = nuxtApp
    const context = { app: nuxtApp }

    $store.registerModuleNuxtSafe('billing', billingStore)

    $registry.register('plugin', new BillingPlugin(context))
    $registry.register('admin', new BillingProvidersAdminType(context))
    $registry.register('admin', new BillingPlansAdminType(context))
    $registry.register(
      'membersPagePlugins',
      new BillingMembersPagePluginType(context)
    )
  },
})
