import { AdminType } from '@baserow/modules/core/adminTypes'

export class BillingAdminType extends AdminType {
  static getType() {
    return 'billing'
  }

  getIconClass() {
    return 'iconoir-credit-card'
  }

  getName() {
    const { $i18n: i18n } = this.app
    return i18n.t('billing.adminType.name')
  }

  getCategory() {
    const { $i18n: i18n } = this.app
    return i18n.t('billing.adminType.category')
  }

  getRouteName() {
    return 'admin-billing'
  }

  getOrder() {
    return 50
  }
}
