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

        <div v-for="(item, index) in fus" :key="index" class="container">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">{{ item.time }}</h5>
              <p class="card-text">{{ item.question }}</p>
              <div class="row">
                <div class="col">
                  <p class="card-text">覆图：</p>
                  <img :src="item.img_question" :alt="item.imageAlt1" class="img-fluid" style="max-width: 200px; max-height: 200px;">
                </div>
                <div class="col">
                  <p class="card-text">答案：</p>
                  <img :src="item.img_answer" :alt="item.imageAlt2" class="img-fluid" style="max-width: 200px; max-height: 200px;">
                </div>
              </div>
              <p class="card-text">结果：</p>
              
              <!-- <div v-if="!item.editing">
                <p class="card-text">{{ item.answer }}</p>
                <button @click="startEditing(index)" class="btn btn-primary">Modify</button>
                <button @click="delete(index)" class="btn btn-danger">Delete</button>
              </div>
              <div v-else>
                <textarea v-model="item.editedAnswer" class="form-control"></textarea>
                <button @click="confirmEdit(index)" class="btn btn-success">Confirm</button>
                <button @click="cancelEdit(index)" class="btn btn-secondary">Cancel</button>
              </div> -->

              <div v-if="item.answer && !item.editing">                
                <p class="card-text">{{ item.answer }}</p>
                <div class="btn-group" role="group">
                    <button @click="startEditing(index)" type="update" class="btn btn-warning btn-sm">修改</button>
                    <button @click="deleteItem(index)" type="delete" class="btn btn-danger btn-sm">删除</button>
                </div>                
              </div>
              <div v-else>              
                <input v-model="item.editedAnswer" class="form-control" type="text" placeholder="在这里输入物品名称，性质，材料，形状等关键词">
                <button @click="confirmEdit(index)" class="btn btn-success">确认</button>
                <button @click="cancelEdit(index)" class="btn btn-secondary">取消</button>
              </div>            

            </div>
          </div>
        </div>

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
import DateSelector from './DateSelector.vue';
import moment from 'moment';
import 'moment-timezone';


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
      const host = 'http://max65536.com';
      // const host = 'http://localhost:5000';
      const path = host+'/api/fus';
      // console.log(this.page);
      // console.log(this.selectedDate);
      var timefrom = this.selectedDate[0].toISOString();
      var timeto   = this.selectedDate[1].toISOString();
      axios.get(path, {params:{page:this.page, from:timefrom, to:timeto}})
        .then((res) => {
          this.total = res.data.total        
          this.fus = res.data.fus.map(item => {
              return {
                  ...item,
                  time: moment(item.time).tz('Asia/Shanghai'),
                  img_question:host + "/static/images/"+ item.source +"/" + item.img_question,
                  img_answer  :host + "/static/images/" + item.source +"/" + item.img_answer,
                  img_tag:item.img_question,
                  // answer:"answer",
                  editing : false,
                  editedAnswer: item.answer,
              };
          });                 
        })
        .catch((error) => {
          console.error(error);
        });
        console.log(this.fus);
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

    startEditing(index) {
      this.fus[index].editing = true;
      this.fus[index].editedAnswer = this.fus[index].answer;
    },
    confirmEdit(index) {
      const editedAnswer = this.fus[index].editedAnswer;
      // Perform the necessary logic to save the edited answer
      const host = 'http://localhost:5000';
      const postData = {
        answer: this.fus[index].editedAnswer,
        image_question: this.fus[index].img_tag
      };
      console.log('Edited Answer:', editedAnswer);
      axios.post(host + '/api/edit_answer', postData)
      .then(response => {
        // 处理成功响应
        console.log(postData);
        console.log(response.data);
        this.fus[index].editing = false;
        this.fus[index].answer = editedAnswer;
      })
      .catch(error => {
        // 处理错误响应
        console.error(error);
      });

    },
    cancelEdit(index) {
      // Reset editing state without saving changes
      this.fus[index].editing = false;
    },
    deleteItem(index) {
      // Handle delete button click for specific item
      console.log('Delete item at index:', index);
    },

  },
  created() {
    this.getFus();
    console.log("show response");
    console.log(this.fus);
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