/**
 * Created by lij021 on 2019/7/1.
 */

import httpRequest from '@/libs/httpRequest'
/* eslint-disable */
export const downloadConfig = (host, type, inventory) => {
  return httpRequest.request({
    url: '/api/download_config',
    method: 'get',
    params: {
      host,
      type,
      inventory
    }
  })
}

export const getConfig = (filename, type) => {
  return httpRequest.request({
    url: '/api/get_config',
    method: 'get',
    params: {
      filename,
      type
    }
  })
}

export const uploadConfig = (type, host, inventory, content, reset) => {
  return httpRequest.request({
    url: '/api/upload_config',
    method: 'post',
    params: {
      type,
      inventory,
      host,
      reset
    },
    data: content
  })
}

export const getTask = (id) => {
  return httpRequest.request({
    url: '/api/get_task',
    method: 'get',
    params: {"id": id}
  })
}



