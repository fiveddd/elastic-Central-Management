import httpRequest from '@/libs/httpRequest'
/* eslint-disable */
export const listInventory = () => {
  return httpRequest.request({
    url: '/api/list_invetory',
    method: 'get'
  })
}

export const getInventory = (name,type) => {
  return httpRequest.request({
    url: '/api/get_invetory',
    method: 'get',
    params: {"name": name,"type":type}
  })
}
