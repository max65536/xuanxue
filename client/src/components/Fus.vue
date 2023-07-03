<template>
  <div>
      
      <dateselector @date-selected="handleDateSelected" />
      <!-- <p>选中的日期：{{ selectedDate }}</p> -->
  </div>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>射覆记录</h1>
        <hr><br><br>
        <!-- <alert :message=message></alert> -->
        <button
          type="button"
          class="btn btn-success btn-sm"
          @click="toggleAddBookModal">
          添加记录
        </button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">日期</th>
              <th scope="col">问题描述</th>
              <th scope="col">出覆</th>
              <th scope="col">覆底</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(fu, index) in fus" :key="index">
              <td>{{ fu.time }}</td>
              <td>{{ fu.question }}</td>
              <!-- <td>{{ fu.img_question }}</td> -->
              <td><img :src="fu.img_question" alt="Image" style="max-width: 100px; max-height: 100px;"></td>             
              <td><img :src="fu.img_answer" alt="Image" style="max-width: 100px; max-height: 100px;"></td> 
              <!-- <td>{{ fu.wang }}</td> -->
              <td>
                <div class="btn-group" role="group">
                  <button type="update" class="btn btn-warning btn-sm">修改</button>
                  <button type="delete" class="btn btn-danger btn-sm">删除</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
  <paginate
     v-model="page"
    :page-count="total"
    :page-range="3"
    :margin-pages="2"
    :click-handler="clickCallback"
    :prev-text="'<'"
    :next-text="'>'"
    :container-class="'pagination'"
    :page-class="'page-item'"
      />
</template>

<script>
import axios from 'axios';
import Paginate from 'vuejs-paginate-next';
import DateSelector from './DateSelector.vue'

export default {
  data() {
    return {
      fus: [],
      total:0,
      page:1,
      selectedDate: [new Date(2022, 10, 10, 10, 10), new Date(2023, 11, 11, 10, 10)]
    };
  },
  components:{
      paginate:Paginate,
      dateselector:DateSelector,
  },
  methods: {
    getFus() {
      const host = 'http://localhost:5000';
      const path = host+'/api/fus';
      console.log(this.page);
      console.log(this.selectedDate);
      var timefrom = this.selectedDate[0].toISOString()
      var timeto   = this.selectedDate[1].toISOString()
      axios.get(path, {params:{page:this.page, from:timefrom, to:timeto}})
        .then((res) => {
          this.total = res.data.total        
          this.fus = res.data.fus.map(item => {
              return {
                  ...item,
                  img_question:host + "/static/images/"+ item.source +"/" + item.img_question,
                  img_answer  :host + "/static/images/" + item.source +"/" + item.img_answer,
              };
          });                 
        })
        .catch((error) => {
          console.error(error);
        });
    },
    clickCallback (pageNum) {
      // console.log(pageNum);
      
      this.getFus();
    },      
    handleDateSelected(value) {
    // 在父组件中接收选中的日期值
      this.selectedDate = value;
      this.getFus();
    },      
  },
  created() {
    this.getFus();
  }
};
</script>


<style>
.pagination {
display: flex;
justify-content: center;
align-items: center;
margin-top: 20px; /* 根据需要调整上下边距 */
}
</style>