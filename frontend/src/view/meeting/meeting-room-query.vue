<template>
  <Form ref="meetingroom" :model="meetingroom" :rules='ruleValidate' :label-width="120">
    <FormItem label="参会人数" prop="capacity">
      <InputNumber :max="100" :min="0" v-model="meetingroom.capacity"></InputNumber>
    </FormItem>
    <FormItem label="需要投影仪" prop="hasProjector">
      <Select v-model="meetingroom.hasProjector">
        <Option value="false">否</Option>
        <Option value="true">是</Option>
      </Select>
    </FormItem>
    <FormItem label="需要视频会议设备" prop="hasRemoteConferenceDevice">
      <Select v-model="meetingroom.hasRemoteConferenceDevice">
        <Option value="false">否</Option>
        <Option value="true">是</Option>
      </Select>
    </FormItem>
    <FormItem label="需要网络接口" prop="hasNetworkCable">
      <Select v-model="meetingroom.hasNetworkCable">
        <Option value="false">否</Option>
        <Option value="true">是</Option>
      </Select>
    </FormItem>
    <FormItem>
      <Button type="primary" @click="handleSubmit('meetingroom')">提交</Button>
      <Button @click="handleReset('meetingroom')" style="margin-left: 8px">重置</Button>
    </FormItem>
    <iv-table border :data="meetingroomlist">
      <iv-table-column label="名称" prop="name"></iv-table-column>
      <iv-table-column label="容量" prop="capacity"></iv-table-column>
      <iv-table-column label="投影仪">
        <span slot-scope="scope">{{scope.row.hasProjector ? '有' : '无'}}</span>
      </iv-table-column>
      <iv-table-column label="视频会议设备">
        <span slot-scope="scope">{{scope.row.hasRemoteConferenceDevice ? '有' : '无'}}</span>
      </iv-table-column>
      <iv-table-column label="网络接口">
        <span slot-scope="scope">{{scope.row.hasNetworkCable ? '有' : '无'}}</span>
      </iv-table-column>
      <iv-table-column label="预定情况" :width="600">
        <ol slot-scope="scope">
          <li v-for="item in scope.row.reservationList" :key="item.id">
            {{getFormattedContent(item)}}
          </li>
        </ol>
      </iv-table-column>
    </iv-table>
  </Form>
</template>
<script>
import { listMeetingRooms } from '@/api/meetingroom'
import { format } from 'date-fns'

export default {
  data () {
    return {
      meetingroom: {
        capacity: 0,
        hasProjector: 'false',
        hasRemoteConferenceDevice: 'false',
        hasNetworkCable: 'false'
      },
      ruleValidate: {
        capacity: [
          { required: true, message: '请输入参会人数', trigger: 'blur' }
        ]
      },
      meetingroomlist: []
    }
  },
  methods: {
    handleSubmit (name) {
      listMeetingRooms(this.meetingroom).then(data => {
        this.meetingroomlist = data.data
        console.log(data)
      })
    },
    handleReset (name) {
      this.$refs[name].resetFields()
    },
    getFormattedContent (item) {
      return `${format(item.startTime, 'YYYY-MM-DD HH:mm')} - ${format(item.endTime, 'YYYY-MM-DD HH:mm')}  ${item.user}  ${item.description}`
    }
  },
  mounted () {
    this.handleSubmit('meetingroom')
  }
}
</script>
