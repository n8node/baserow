import { MembersPagePluginType } from '@baserow/modules/database/membersPagePluginTypes'
import UserPlanField from '@baserow/modules/billing/components/admin/UserPlanField'
import CrudTableColumn from '@baserow/modules/core/crudTable/crudTableColumn'

export class BillingMembersPagePluginType extends MembersPagePluginType {
  static getType() {
    return 'billing_plan'
  }

  mutateAdminUsersTableColumns(columns, context) {
    const moreIdx = columns.findIndex((c) => c.key === 'more')
    const planColumn = new CrudTableColumn(
      'billing_plan_name',
      () => this.app.$i18n.t('billing.usersTable.plan'),
      UserPlanField,
      false
    )
    if (moreIdx !== -1) {
      columns.splice(moreIdx, 0, planColumn)
    } else {
      columns.push(planColumn)
    }
    return columns
  }
}
