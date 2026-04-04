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
    const { $registry, $store, $clientErrorMap, $i18n } = nuxtApp
    const context = { app: nuxtApp }

    $clientErrorMap.setError(
      'ERROR_BILLING_CANNOT_DELETE_DEFAULT_PLAN',
      $i18n.t('billing.admin.errors.cannotDeleteDefaultPlanTitle'),
      $i18n.t('billing.admin.errors.cannotDeleteDefaultPlanDescription')
    )
    $clientErrorMap.setError(
      'ERROR_BILLING_PLAN_HAS_SUBSCRIPTIONS',
      $i18n.t('billing.admin.errors.planHasSubscriptionsTitle'),
      $i18n.t('billing.admin.errors.planHasSubscriptionsDescription')
    )
    $clientErrorMap.setError(
      'ERROR_BILLING_PLAN_NOT_FOUND',
      $i18n.t('billing.admin.errors.planNotFoundTitle'),
      $i18n.t('billing.admin.errors.planNotFoundDescription')
    )

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
