new Vue({
  el: '#starting',
  delimiters: ['${','}'],
  data: {
    loading: false,
    preview: false,
    message: null,
    failedServicesData: '',
  },
  mounted: function() {
  },
  methods: {
    showFailedServices: function() {
      this.$http.get(`/api/v1/services/failed/`)
          .then((response) => {
            this.failedServicesData = response.data;
            $("#showFailedServices").modal('show');
          })
          .catch((err) => {
            console.log(err);
          })
    }
  }
});
