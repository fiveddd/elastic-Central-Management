import Main from '@/view/main'
import ConfigKibana from '@/view/system-config/config-kibana.vue'
import ConfigElasticsearch from '@/view/system-config/config-elasticsearch.vue'
import ConfigLogstash from '@/view/system-config/config-logstash.vue'
import ConfigFilebeat from '@/view/system-config/config-filebeat.vue'
import parentView from '@/components/parent-view'

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
    name: 'elastic配置更新',
    meta: {
      icon: "md-construct",
      title: 'elastic配置更新'
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
        component: parentView,
        children: [
          {
            path: '/configuration/logstash/etc',
            name: 'logstash etc 配置更新',
            meta: {
              icon: 'md-menu',
              title: 'logstash etc 配置更新'
            },
            component: ConfigKibana
          },{
            path: '/configuration/logstash/etc',
            name: 'logstash pattern 配置更新',
            meta: {
              icon: 'md-menu',
              title: 'logstash etc 配置更新'
            },
            component: ConfigKibana
          },{
            path: '/configuration/logstash/etc',
            name: 'logstash pipeline 配置更新',
            meta: {
              icon: 'md-menu',
              title: 'logstash pipeline 配置更新'
            },
            component: ConfigKibana
          }]
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
      name: 'elastic软件更新',
    meta: {
    icon: "md-construct",
      title: 'elastic软件更新'
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
          component: ConfigFilebeat
        }
      ]
  },
  {
    path: '/apm',
    name: 'APM',
    meta: {
      icon: "md-construct",
      title: 'APM'
    },
    component: Main,
    children: [
      {
        path: '/apm/deploy',
        name: 'APM客户端部署',
        meta: {
          icon: 'md-menu',
          title: 'APM客户端部署'
        },
        component: ConfigKibana
      },
      {
        path: '/apm/configuration',
        name: 'APM配置更新',
        meta: {
          icon: 'md-menu',
          title: 'APM配置更新'
        },
        component: ConfigElasticsearch
      }
    ]
  },
  {
    path: '/kafka',
    name: 'kafka',
    meta: {
      icon: "md-construct",
      title: 'kafka'
    },
    component: Main,
    children: [
      {
        path: '/kafka/deploy',
        name: 'kafka部署',
        meta: {
          icon: 'md-menu',
          title: 'kafka部署'
        },
        component: ConfigKibana
      },
      {
        path: '/kafka/configuration',
        name: 'kafka配置更新',
        meta: {
          icon: 'md-menu',
          title: 'kafka配置更新'
        },
        component: ConfigElasticsearch
      }
    ]
  },
  {
    path: '/zookeeper',
    name: 'zookeeper',
    meta: {
      icon: "md-construct",
      title: 'zookeeper'
    },
    component: Main,
    children: [
      {
        path: '/zookeeper/deploy',
        name: 'zookeeper部署',
        meta: {
          icon: 'md-menu',
          title: 'zookeeper部署'
        },
        component: ConfigKibana
      },
      {
        path: '/zookeeper/configuration',
        name: 'zookeeper配置更新',
        meta: {
          icon: 'md-menu',
          title: 'zookeeper配置更新'
        },
        component: ConfigElasticsearch
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
