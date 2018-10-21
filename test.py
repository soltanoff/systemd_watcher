import subprocess
import re

class SYSTEMCTL_COMMANDS:
    STATUS_ALL = 'systemctl status'
    STATUS = 'systemctl status {0}'
    START = 'systemctl start {0}'
    RESTART = 'systemctl restart {0}'
    STOP = 'systemctl stop {0}'
    FAILED = 'systemctl --failed'


class ServiceMonitor:
    __SERVICE_PATTERN = re.compile('─(.*\.service)')

    def __exec(self, cmd):
        return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()[0].decode('utf-8')

    def get_status_all(self):
        return self.__exec(SYSTEMCTL_COMMANDS.STATUS_ALL)

    def get_service_status(self, service_name):
        return self.__exec(SYSTEMCTL_COMMANDS.STATUS.format(service_name))

    def get_failed_services(self):
        return self.__exec(SYSTEMCTL_COMMANDS.FAILED)

    def get_service_list(self):
        return re.findall(self.__SERVICE_PATTERN, self.get_status_all())

    def iter_service_list(self):
        return re.finditer(self.__SERVICE_PATTERN, self.get_status_all())

    def set_start_service(self, service_name):
        return self.__exec(SYSTEMCTL_COMMANDS.START.format(service_name))

    def set_restart_service(self, service_name):
        return self.__exec(SYSTEMCTL_COMMANDS.RESTART.format(service_name))

    def set_stop_service(self, service_name):
        return self.__exec(SYSTEMCTL_COMMANDS.STOP.format(service_name))



if __name__ == '__main__':
    monitor = ServiceMonitor()
    print(monitor.get_service_list())
    print(monitor.get_failed_services())
    for x in monitor.get_service_list():
        print(monitor.get_service_status(x))
