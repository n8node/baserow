import { BaserowPlugin } from '@baserow/modules/core/plugins'
import SubscriptionBadge from '@baserow/modules/billing/components/SubscriptionBadge'
import SidebarBillingLink from '@baserow/modules/billing/components/SidebarBillingLink'

export class BillingPlugin extends BaserowPlugin {
  static getType() {
    return 'billing'
  }

  getHighestLicenseTypeBadge() {
    return SubscriptionBadge
  }

  getDashboardWorkspacePlanBadge() {
    return SubscriptionBadge
  }

  getUserContextComponents() {
    return [SidebarBillingLink]
  }
}
