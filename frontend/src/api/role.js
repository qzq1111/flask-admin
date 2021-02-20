import request from '@/utils/request'


export function getRoleLabels() {
  return request({
    url: '/v1/role/labels',
    method: 'get'
  })
}

export function getRoleList(data) {
  return request({
    url: '/v1/role/list',
    method: 'get',
    params: data
  })
}

export function changeRoleStatus(role_id, data) {
  return request({
    url: `/v1/role/${role_id}/status`,
    method: 'put',
    data
  })
}
