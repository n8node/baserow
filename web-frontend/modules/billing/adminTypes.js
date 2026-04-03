import { AdminType } from '@baserow/modules/core/adminTypes'

export class BillingProvidersAdminType extends AdminType {
  static getType() {
    return 'billing-providers'
  }

  getIconClass() {
    return 'iconoir-credit-card'
  }

  getName() {
    const { $i18n: i18n } = this.app
    return i18n.t('billing.adminType.providers')
  }

  getCategory() {
    const { $i18n: i18n } = this.app
    return i18n.t('billing.adminType.category')
  }

  getRouteName() {
    return 'admin-billing-providers'
  }

  getOrder() {
    return 50
  }
}

export class BillingPlansAdminType extends AdminType {
  static getType() {
    return 'billing-plans'
  }

  getIconClass() {
    return 'iconoir-list'
  }

  getName() {
    const { $i18n: i18n } = this.app
    return i18n.t('billing.adminType.plans')
  }

  getCategory() {
    const { $i18n: i18n } = this.app
    return i18n.t('billing.adminType.category')
  }

  getRouteName() {
    return 'admin-billing-plans'
  }

  getOrder() {
    return 51
  }
}
