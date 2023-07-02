<template>
    <div class="container">
      <div class="row">
        <div class="col-sm-10">
          <h1>射覆记录</h1>
          <hr><br><br>
          <alert :message=message></alert>
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
                <td>{{ fu.date }}</td>
                <td>{{ fu.question }}</td>
                <td>{{ fu.img_qestion }}</td>
                <td>{{ fu.img_answer }}</td>
                <td>{{ fu.wang }}</td>
                <td>
                  <div class="btn-group" role="group">
                    <button type="修改" class="btn btn-warning btn-sm">Update</button>
                    <button type="删除" class="btn btn-danger btn-sm">Delete</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
  
      <!-- add new book modal -->
      <div
        ref="addBookModal"
        class="modal fade"
        :class="{ show: activeAddBookModal, 'd-block': activeAddBookModal }"
        tabindex="-1"
        role="dialog">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Add a new book</h5>
              <button
                type="button"
                class="close"
                data-dismiss="modal"
                aria-label="Close"
                @click="toggleAddBookModal">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div class="modal-body">
              <form>
                <div class="mb-3">
                  <label for="addBookTitle" class="form-label">Title:</label>
                  <input
                    type="text"
                    class="form-control"
                    id="addBookTitle"
                    v-model="addBookForm.title"
                    placeholder="Enter title">
                </div>
                <div class="mb-3">
                  <label for="addBookAuthor" class="form-label">Author:</label>
                  <input
                    type="text"
                    class="form-control"
                    id="addBookAuthor"
                    v-model="addBookForm.author"
                    placeholder="Enter author">
                </div>
                <div class="mb-3 form-check">
                  <input
                    type="checkbox"
                    class="form-check-input"
                    id="addBookRead"
                    v-model="addBookForm.read">
                  <label class="form-check-label" for="addBookRead">Read?</label>
                </div>
                <div class="btn-group" role="group">
                  <button
                    type="button"
                    class="btn btn-primary btn-sm"
                    @click="handleAddSubmit">
                    Submit
                  </button>
                  <button
                    type="button"
                    class="btn btn-danger btn-sm"
                    @click="handleAddReset">
                    Reset
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
      <div v-if="activeAddBookModal" class="modal-backdrop fade show"></div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import Alert from './Alert.vue'
  
  export default {
    data() {
      return {
        activeAddBookModal: false,
        addBookForm: {
          title: '',
          author: '',
          read: [],
        },
        fus: [],
      };
    },
    components: {
        alert: Alert,
    },
    methods: {
      addBook(payload) {
        const path = 'http://localhost:5000/test';
        axios.post(path, payload)
          .then(() => {
            this.getBooks();
            this.message = 'Book added!';
            this.showMessage = true;
          })
          .catch((error) => {
            console.log(error);
            this.getBooks();
          });
      },
      getBooks() {
        const path = 'http://localhost:5000/test';
        axios.get(path)
          .then((res) => {
            this.fus = res.data.fus;
          })
          .catch((error) => {
            console.error(error);
          });
      },
      handleAddReset() {
        this.initForm();
      },
      handleAddSubmit() {
        this.toggleAddBookModal();
        let read = false;
        if (this.addBookForm.read[0]) {
          read = true;
        }
        const payload = {
          title: this.addBookForm.title,
          author: this.addBookForm.author,
          read, // property shorthand
        };
        this.addBook(payload);
        this.initForm();
      },
      initForm() {
        this.addBookForm.title = '';
        this.addBookForm.author = '';
        this.addBookForm.read = [];
      },
      toggleAddBookModal() {
        const body = document.querySelector('body');
        this.activeAddBookModal = !this.activeAddBookModal;
        if (this.activeAddBookModal) {
          body.classList.add('modal-open');
        } else {
          body.classList.remove('modal-open');
        }
      },
    },
    created() {
      this.getBooks();
    },
  };
  </script>