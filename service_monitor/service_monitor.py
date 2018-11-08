import re
import subprocess


class SYSTEMCTL_COMMANDS:
    STATUS_ALL = 'systemctl status'
    STATUS = 'systemctl status {0}'
    START = 'systemctl start {0}'
    RESTART = 'systemctl restart {0}'
    STOP = 'systemctl stop {0}'
    FAILED = 'systemctl --failed'


class ServiceMonitor:
    __SERVICE_PATTERN = re.compile('─(.*\.service)')
    __NAME_PATTERN = re.compile(r"^●?\s?.*\s-\s(.*)\n")
    __SERVICE_NAME_PATTERN = re.compile(r"^●?\s?(.*)\s-")
    __STATUS_PATTERN = re.compile(r"Active:\s(.*)\n")
    __DESCRIPTION_PATTERN = re.compile(
        r"(^\s+Loaded:\s.*\n|^\s+Process:\s.*\n|^\s+Main PID:\s.*\n|^\s+CGroup:\s.*(\n.*)+\n\n)",
        re.MULTILINE
    )

    @staticmethod
    def __exec(cmd):
        return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()[0].decode('utf-8')

    def __get_failed_services(self):
        return self.__exec(SYSTEMCTL_COMMANDS.FAILED)

    def __get_service_list(self):
        return re.findall(self.__SERVICE_PATTERN, self.get_status_all())

    def get_status_all(self):
        return self.__exec(SYSTEMCTL_COMMANDS.STATUS_ALL)

    def __get_service_status(self, service_name):
        return self.__exec(SYSTEMCTL_COMMANDS.STATUS.format(service_name))

    def extract_data(self, data):
        return {
            'name': re.findall(self.__NAME_PATTERN, data)[0],
            'service_name': re.findall(self.__SERVICE_NAME_PATTERN, data)[0],
            'status': re.findall(self.__STATUS_PATTERN, data)[0],
            'description': ''.join(map(lambda x: x[0], re.findall(self.__DESCRIPTION_PATTERN, data)))
        }

    def iter_service_list(self):
        for status in filter(bool, map(self.__get_service_status, self.__get_service_list())):
            yield self.extract_data(status)

    def get_failed_services(self):
        return self.__get_failed_services()

    def get_service_list(self):
        return list(self.iter_service_list())

    def get_service_status(self, service_name):
        return self.extract_data(self.__get_service_status(service_name))

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
