export default (client) => ({
  fetchBlocks(locale) {
    return client.get('/admin/landing/blocks/', { params: { locale } })
  },
  create(values) {
    return client.post('/admin/landing/blocks/', values)
  },
  update(id, values) {
    return client.patch(`/admin/landing/blocks/${id}/`, values)
  },
  delete(id) {
    return client.delete(`/admin/landing/blocks/${id}/`)
  },
})
