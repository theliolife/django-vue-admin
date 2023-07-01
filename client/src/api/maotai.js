import request from '@/utils/request'

export function maotai_list(data) {
  return request({
    url: '/maotai/list',
    method: 'get',
    data
  })
}
