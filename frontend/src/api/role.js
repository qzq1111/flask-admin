import request from '@/utils/request'


export function getRoleLabels() {
    return request({
      url: '/v1/role/labels',
      method: 'get'
    })
  }
  