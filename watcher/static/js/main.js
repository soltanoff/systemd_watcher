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
            this.getServicesByPickedRadioButton(value);
        }
    },
    methods: {
        getServices: function() {
            this.loading = true;
            this.$http.get('/api/v1/services/')
            .then((response) => {
                this.loading = false;
                this.services = response.data;
            })
            .catch((err) => {
                this.loading = false;
                console.log(err);
            })
        },
        getActiveServices: function() {
            this.loading = true;
            this.$http.get('/api/v1/services/active/')
            .then((response) => {
                this.loading = false;
                this.services = response.data;
            })
            .catch((err) => {
                this.loading = false;
                console.log(err);
            })
        },
        getServicesByPickedRadioButton: function(value) {
            if (value == 'enabled') {
                this.getServices();
            }
            else {
                this.getActiveServices();
            }
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
            this.loading = true;
            this.$http.post('/api/v1/service/start/' + service + '/')
            .then((response) => {
                this.serviceStatus = "Service \"<b>" + service + "</b>\" started successful!";
                this.getServicesByPickedRadioButton(pickedServices);
                $("#showServiceStatus").modal('show');
            })
            .catch((err) => {
                console.log(err);
                this.serviceStatus = "Service \"<b>" + service + "</b>\" not started!<br>Error: " + err;
                this.getServicesByPickedRadioButton(pickedServices);
                $("#showServiceStatus").modal('show');
            })
        },
        restartService: function(service) {
            this.loading = true;
            this.$http.post('/api/v1/service/restart/' + service + '/')
            .then((response) => {
                this.serviceStatus = "Service \"<b>" + service + "</b>\" restarted successful!";
                this.getServicesByPickedRadioButton(pickedServices);
                $("#showServiceStatus").modal('show');
            })
            .catch((err) => {
                console.log(err);
                this.serviceStatus = "Service \"<b>" + service + "</b>\" not restarted!<br>Error: " + err;
                this.getServicesByPickedRadioButton(pickedServices);
                $("#showServiceStatus").modal('show');
            })
        },
        stopService: function(service) {
            this.loading = true;
            this.$http.post('/api/v1/service/stop/' + service + '/')
            .then((response) => {
                this.serviceStatus = "Service \"<b>" + service + "</b>\" stopped!";
                this.getServicesByPickedRadioButton(pickedServices);
                $("#showServiceStatus").modal('show');
            })
            .catch((err) => {
                console.log(err);
                this.serviceStatus = "Service \"<b>" + service + "</b>\" not stopped!<br>Error: " + err;
                this.getServicesByPickedRadioButton(pickedServices);
                $("#showServiceStatus").modal('show');
            })
        },
    }
});
