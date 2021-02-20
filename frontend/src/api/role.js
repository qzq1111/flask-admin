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

export function addRole(data) {
  return request({
    url: `/v1/role`,
    method: 'post',
    data
  })
}

export function getRoleById(role_id) {
  return request({
    url: `/v1/role/${role_id}`,
    method: 'get'
  })
}

export function getRoleCheckMenus(role_id) {
  return request({
    url: `/v1/role/${role_id}/check`,
    method: 'get'
  })
}

export function updateRole(role_id,data) {
  return request({
    url: `/v1/role/${role_id}`,
    method: 'put',
    data
  })
}

