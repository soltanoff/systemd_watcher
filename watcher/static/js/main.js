new Vue({
    el: '#app',
    delimiters: ['${','}'],
    data: {
        loading: false,
        preview: false,
        pickedServices: 'enabled',
        message: null,
        serviceStatus: '',
        failedServicesData: '',
        services: [],
    },
    mounted: function() {
        this.getServices();
    },
    watch: {
        pickedServices: function(value) {
            if (value == 'enabled') {
                this.getServices();
            }
            else {
                this.getActiveServices();
            }
        }
    },
    methods: {
        getServices: function() {
            this.$http.get('/api/v1/services/')
            .then((response) => {
                this.services = response.data;
            })
            .catch((err) => {
                console.log(err);
            })
        },
        getActiveServices: function() {
            this.$http.get('/api/v1/services/active/')
            .then((response) => {
                this.services = response.data;
            })
            .catch((err) => {
                console.log(err);
            })
        },
        showFailedServices: function() {
            this.$http.get('/api/v1/services/failed/')
            .then((response) => {
                this.failedServicesData = response.data;
                $("#showFailedServices").modal('show');
            })
            .catch((err) => {
                console.log(err);
            })
        },
        startService: function(service) {
            this.$http.post('/api/v1/service/start/' + service + '/')
            .then((response) => {
                this.serviceStatus = "Service \"<b>" + service + "</b>\" started successful!";
                this.getServices();
                $("#showServiceStatus").modal('show');
            })
            .catch((err) => {
                console.log(err);
                this.serviceStatus = "Service \"<b>" + service + "</b>\" not started!<br>Error: " + err;
                this.getServices();
                $("#showServiceStatus").modal('show');
            })
        },
        restartService: function(service) {
            this.$http.post('/api/v1/service/restart/' + service + '/')
            .then((response) => {
                this.serviceStatus = "Service \"<b>" + service + "</b>\" restarted successful!";
                this.getServices();
                $("#showServiceStatus").modal('show');
            })
            .catch((err) => {
                console.log(err);
                this.serviceStatus = "Service \"<b>" + service + "</b>\" not restarted!<br>Error: " + err;
                this.getServices();
                $("#showServiceStatus").modal('show');
            })
        },
        stopService: function(service) {
            this.$http.post('/api/v1/service/stop/' + service + '/')
            .then((response) => {
                this.serviceStatus = "Service \"<b>" + service + "</b>\" stopped!";
                this.getServices();
                $("#showServiceStatus").modal('show');
            })
            .catch((err) => {
                console.log(err);
                this.serviceStatus = "Service \"<b>" + service + "</b>\" not stopped!<br>Error: " + err;
                this.getServices();
                $("#showServiceStatus").modal('show');
            })
        },
    }
});
