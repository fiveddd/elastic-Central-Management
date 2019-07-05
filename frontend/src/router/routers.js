import Main from '@/view/main'
import ConfigKibana from '@/view/system-config/config-kibana.vue'
import ConfigElasticsearch from '@/view/system-config/config-elasticsearch.vue'
import ConfigLogstash from '@/view/system-config/config-logstash.vue'
import ConfigFilebeat from '@/view/system-config/config-filebeat.vue'

/**
 * iview-admin中meta除了原生参数外可配置的参数:
 * meta: {
 *  hideInMenu: (false) 设为true后在左侧菜单不会显示该页面选项
 *  notCache: (false) 设为true后页面不会缓存
 *  access: (null) 可访问该页面的权限数组，当前路由设置的权限会影响子路由
 *  icon: (-) 该页面在左侧菜单、面包屑和标签导航处显示的图标，如果是自定义图标，需要在图标名称前加下划线'_'
 * }
 */

const OverView = { template: '<div><h1>Welcome!</h1><p>Here is what site is about.</p></div>' }

export default [
  {
    path: '/',
    name: '_home',
    redirect: 'home',
    component: Main,
    meta: {
      hideInMenu: true,
      notCache: true
    },
    children: [
      {
        path: '/home',
        name: 'home',
        meta: {
          hideInMenu: true,
          title: '首页',
          notCache: true
        },
        component: ConfigKibana
      },
    ]
  },
  {
    path: '/configuration',
    name: '配置更新',
    meta: {
      icon: "md-construct",
      title: '配置更新'
    },
    component: Main,
    children: [
      {
        path: '/kibana',
        name: 'kibana配置更新',
        meta: {
          icon: 'md-menu',
          title: 'kibana配置更新'
        },
        component: ConfigKibana
      },
      {
        path: '/elasticsearch',
        name: 'elasticsearch配置更新',
        meta: {
          icon: 'md-menu',
          title: 'elasticsearch配置更新'
        },
        component: ConfigElasticsearch
      },
      {
        path: '/logstash',
        name: 'logstash配置更新',
        meta: {
          icon: 'md-menu',
          title: 'logstash配置更新'
        },
        component: ConfigLogstash
      },
      {
        path: '/filebeat',
        name: 'filebeat配置更新',
        meta: {
          icon: 'md-menu',
          title: 'filebeat配置更新'
        },
        component: ConfigFilebeat
      }
    ]
  },
  {
    path: '/configuration',
      name: '软件更新',
    meta: {
    icon: "md-construct",
      title: '软件更新'
  },
    component: Main,
      children: [
        {
          path: '/kibana',
          name: 'kibana软件更新',
          meta: {
            icon: 'md-menu',
            title: 'kibana软件更新'
          },
          component: ConfigKibana
        },
        {
          path: '/elasticsearch',
          name: 'elasticsearch软件更新',
          meta: {
            icon: 'md-menu',
            title: 'elasticsearch软件更新'
          },
          component: ConfigElasticsearch
        },
        {
          path: '/logstash',
          name: 'logstash软件更新',
          meta: {
            icon: 'md-menu',
            title: 'logstash软件更新'
          },
          component: ConfigLogstash
        },
        {
          path: '/filebeat',
          name: 'filebeat软件更新',
          meta: {
            icon: 'md-menu',
            title: 'filebeat软件更新'
          },
          component: ConfigLogstash
        }
      ]
  },

  {
    path: '/overview',
    name: 'overview',
    component: OverView
  },
  {    path: '/configuration',
    name: '一键破解',
    meta: {
      icon: "md-construct",
      title: '一键破解'
    },
    component: Main
  },
  {
    path: '/401',
    name: 'error_401',
    component: () => import('@/view/error-page/401.vue')
  },
  {
    path: '/500',
    name: 'error_500',
    component: () => import('@/view/error-page/500.vue')
  },
  {
    path: '*',
    name: 'error_404',
    component: () => import('@/view/error-page/404.vue')
  }
]
