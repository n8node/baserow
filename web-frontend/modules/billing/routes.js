import path from 'path'

export const routes = [
  {
    name: 'billing-root',
    path: '',
    file: path.resolve(__dirname, 'pages/root.vue'),
    children: [
      {
        name: 'admin-billing-providers',
        path: '/admin/billing/providers',
        file: path.resolve(__dirname, 'pages/admin/providers.vue'),
      },
      {
        name: 'admin-billing-plans',
        path: '/admin/billing/plans',
        file: path.resolve(__dirname, 'pages/admin/plans.vue'),
      },
    ],
  },
]
