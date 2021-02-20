import request from '@/utils/request'


export function getMenuLabels() {
    return request({
      url: '/v1/menu/labels',
      method: 'get'
    })
  }
  
