import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/v1/user/login',
    method: 'post',
    data
  })
}

export function getInfo() {
  return request({
    url: '/v1/user/info',
    method: 'get'
  })
}

export function logout() {
  return request({
    url: '/v1/user/logout',
    method: 'post'
  })
}

export function getUserList(data) {
  return request({
    url: '/v1/user/list',
    method: 'get',
    params: data
  })
}

export function changeUserStatus(user_id,data){
  return request({
    url: `/v1/user/${user_id}/status`,
    method: 'put',
    data
  })
}