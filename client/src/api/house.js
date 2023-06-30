import request from '@/utils/request'

export function houseDashboard(data) {
  return request({
    url: '/house/dashboard',
    method: 'get',
    data
  })
}
