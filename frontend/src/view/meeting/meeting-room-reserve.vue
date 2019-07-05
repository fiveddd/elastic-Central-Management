<template>
  <Form ref="reservation" :model="reservation" :rules="ruleValidate" :label-width="120">
    <FormItem prop="roomId" label="会议室">
      <Select v-model="reservation.roomId">
        <Option v-for="room in roomList" :value="room.id" :key="room.id">{{ room.name }}</Option>
      </Select>
    </FormItem>
    <FormItem label="会议主题" prop="description">
      <Input type="text" v-model="reservation.description"></Input>
    </FormItem>
    <FormItem label="开始日期" prop="startTime">
      <DatePicker type="datetime" format="yyyy-MM-dd HH:mm" v-model="reservation.startTime"></DatePicker>
    </FormItem>
    <FormItem label="结束日期" prop="endTime">
      <DatePicker type="datetime" format="yyyy-MM-dd HH:mm" v-model="reservation.endTime"></DatePicker>
    </FormItem>
    <FormItem>
      <Button type="primary" @click="handleSubmit('reservation')">提交</Button>
      <Button @click="handleReset('reservation')" style="margin-left: 8px">重置</Button>
    </FormItem>
  </Form>
</template>
<script>
import { reserve, listMeetingRooms } from '@/api/meetingroom'
import { getUser } from '../../libs/util'

export default {
  data () {
    return {
      reservation: {
        roomId: '',
        user: getUser().userName,
        description: '',
        startTime: new Date(),
        endTime: new Date()
      },
      ruleValidate: {
        roomId: [{ required: true, message: '请选择会议室' }],
        description: [
          { required: true, message: '请输入会议内容', trigger: 'blur' },
          { type: 'string', min: 3, message: '至少3个字', trigger: 'blur' }
        ],
        startTime: [{ required: true, message: '请选择会议开始时间' }],
        endTime: [{ required: true, message: '请选择会议结束时间' }]
      },
      roomList: []
    }
  },
  mounted () {
    this.init()
  },
  methods: {
    init () {
      listMeetingRooms({ capacity: -1, hasProjector: false, hasRemoteConferenceDevice: false, hasNetworkCable: false }).then((response) => {
        if (response.status === 200) {
          this.roomList = response.data
        }
      })
    },
    handleSubmit (name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          reserve(this.reservation).then((response) => {
            if (response.status === 200) {
              this.$Message.success('会议室预定成功')
            } else {
              this.$Message.error('预定失败:' + response.status + ',' + response.message)
            }
          })
        } else {
          this.$Message.error('表单数据不合法!')
        }
      })
    },
    handleReset (name) {
      this.$refs[name].resetFields()
    }
  }
}
</script>
