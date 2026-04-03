export default (client) => ({
  fetchBlocks(locale) {
    return client.get('/landing/blocks/', { params: { locale } })
  },
})
