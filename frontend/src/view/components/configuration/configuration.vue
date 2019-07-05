<template>
    <div>
        <Tabs :value="inventoryName" @on-click="get_inventory">
            <TabPane :label="infor" v-for="(infor, i) in inventoryList" :key="`infor-${i}`" :name="infor">
                <Card :bordered="false" v-for="(hosts, group) in inventoryData" :key="group">
                    <p slot="title" style="height: 35px">{{group}}
                        <Button type="circle" icon="md-download" @click="download_config(group)"></Button>
                    </p>
                    <Button type="primary" @click="get_config(host.name)" shape="circle" icon="md-laptop"
                            v-for="(host,i) in hosts" :key="i">{{host.name}}
                    </Button>
                </Card>
            </TabPane>
        </Tabs>
        <Drawer title="运行状态" :closable="false" v-model="showStatusDrawer" width="360">
            <div v-html="runningStatus">
                <Icon type="ios-loading"/>
            </div>
            <div v-html="runningResult"></div>
        </Drawer>
        <Drawer :title="selectedHost+' : '+componentType+'.yml'" :closable="false" placement="left" width="800"
                v-model="showContentDrawer">
            <editor v-model="configurationContent" @init="editorInit" lang="yaml" theme="chrome" width="100%"
                    height="70%"></editor>
            <div class="demo-drawer-footer">
                <Button style="margin-right: 8px" @click="upload_config(false)">上传</Button>
                <Button type="primary" @click="upload_config(true)">上传并重启</Button>
            </div>
        </Drawer>
    </div>
</template>

<script>
/* eslint-disable */
    import {listInventory, getInventory} from '@/api/inventory'
    import {downloadConfig, getConfig, uploadConfig, uploadResetConfig, getTask} from '@/api/configuration'
    import {checkHTTPStatus} from '@/libs/util'
    export default {
      name: 'configuration',
      components: {
        editor: require('vue2-ace-editor')
      },
      props: [
        'componentType'
      ],
      data () {
        return {
          selectedHost: "",
          showStatusDrawer: false,
          showContentDrawer: false,
          taskId: 0,
          runningStatus: "",
          runningResult: "",
          inventoryName: "",
          configurationContent: "",
          hostName: "",
          inventoryList: [],
          inventoryData: []
        }
      },
      mounted () {
        this.list_inventory()
      },
      methods: {
        editorInit: function () {
          require('brace/ext/language_tools') //language extension prerequsite...
          require('brace/mode/yaml')
          require('brace/theme/chrome')
        },
        list_inventory() {
          listInventory().then(data => {
            this.inventoryList = data.data
            this.inventoryName = this.inventoryList[0]
            this.get_inventory(this.inventoryList[0])
          })
        },
        get_inventory(inventoryName) {
          this.inventoryName = inventoryName
          getInventory(inventoryName, this.componentType).then(data => {
            this.inventoryData = data.data
          })
        },
        download_config(group) {
          this.showStatusDrawer = true;
          this.runningStatus = "开始运行任务"
          this.runningResult = ""
          this.hostName = group
          this.$Spin.show()
          downloadConfig(this.hostName, this.componentType, this.inventoryName).then(data => {
            this.$Spin.hide()
            if (checkHTTPStatus(data, this.$Message)) {
              let result = data.data
              this.runningStatus = ""
              for (let k in result.message) {
                this.runningResult += result.message[k]
              }
            } else {
              this.showStatusDrawer = false
            }
          }).catch((e) => {
            console.log(e)
          })
        },
        get_config(hostName){
          this.showContentDrawer = true
          this.selectedHost = hostName
          getConfig(hostName, this.componentType).then(data => {
            this.configurationContent = data.data
          }).catch((e) => {
            console.log(e)
          })

        },
        upload_config(reset){
          this.showStatusDrawer = true;
          this.$Spin.show()
          this.runningStatus = "开始运行任务"
          this.runningResult = ""
          uploadConfig(this.componentType, this.selectedHost, this.inventoryName, this.configurationContent, reset).then(data => {
            this.$Spin.hide()
            if (checkHTTPStatus(data, this.$Message)) {
              let result = data.data
              this.runningStatus = ""
              for (let k in result.message) {
                this.runningResult += result.message[k]
              }
            } else {
              this.showStatusDrawer = false
            }
          }).catch(
            e => {
              this.$Spin.hide()
              this.$Message.error(e)
            })

        },
        clearTimer(){
        }

      }

    }
</script>

<style>
    .demo-drawer-footer {
        width: 100%;
        position: absolute;
        bottom: 0;
        left: 0;
        border-top: 1px solid #e8e8e8;
        padding: 10px 16px;
        text-align: right;
        background: #fff;
    }
</style>