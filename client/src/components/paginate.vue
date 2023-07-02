<template>
    <paginate
      v-model="page"
      :page-count="20"
      :page-range="3"
      :margin-pages="2"
      @click-handler="clickCallback"
      :prev-text="'Prev'"
      :next-text="'Next'"
      :container-class="'pagination'"
      :page-class="'page-item'"
    >
    </paginate>
  </template>
  
  <!-- <script>
    import Paginate from 'vuejs-paginate-next';
    export default {
      data() {
        return {
          page: 10,
        };
      },
    };
  </script> -->

  <script>
    import Paginate from 'vuejs-paginate-next';
    export default {
      components: {
        paginate: Paginate,
      },
      data(){
        return {
            currentPage: 1,
            perPage:10,
            total:100
        }
      },
      methods: {
        clickCallback (pageNum) {
          console.log(pageNum)
        }
      }
    };
  </script>
  