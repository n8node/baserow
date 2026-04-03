import { BaserowPlugin } from '@baserow/modules/core/plugins'
import Impersonate from '@baserow_premium/components/sidebar/Impersonate'
import HighestLicenseTypeBadge from '@baserow_premium/components/sidebar/HighestLicenseTypeBadge'
import PremiumViewOptions from '@baserow_premium/components/views/PremiumViewOptions'
import PublicViewExport from '@baserow_premium/components/views/PublicViewExport'

export class PremiumPlugin extends BaserowPlugin {
  static getType() {
    return 'premium'
  }

  getImpersonateComponent() {
    return Impersonate
  }

  getHighestLicenseTypeBadge() {
    // When the billing module provides its own SubscriptionBadge, defer to it.
    // The billing plugin registers with type 'billing' and also provides a badge.
    return null
  }

  getAdditionalShareLinkOptions() {
    return [PremiumViewOptions]
  }

  getAdditionalTableHeaderComponents(view, isPublic) {
    return isPublic ? [PublicViewExport] : []
  }

  hasFeature(feature, forSpecificWorkspace) {
    return this.app.$licenseHandler.hasFeature(feature, forSpecificWorkspace)
  }

  /**
   * A hook to provide different action buttons to the premium features modal.
   */
  getPremiumModalButtonsComponent() {
    return null
  }
}
