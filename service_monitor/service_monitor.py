import operator
import re
import subprocess


class SYSTEMCTL_COMMANDS:
    ENABLED_SERVICES = "systemctl list-unit-files | grep enabled | grep -Po \'^.*\.service\'"
    FAILED_SERVICES = 'systemctl --failed'
    STATUS_ALL = 'systemctl status'
    STATUS = 'systemctl status {0}'
    START = 'systemctl start {0}'
    RESTART = 'systemctl restart {0}'
    STOP = 'systemctl stop {0}'


class ServiceMonitor:
    __SERVICE_PATTERN = re.compile("─(.*\.service)")
    __NAME_PATTERN = re.compile(r"^●?\s?.*\s-\s(.*)\n")
    __SERVICE_NAME_PATTERN = re.compile(r"^●?\s?(.*\.service)\s-?")
    __STATUS_PATTERN = re.compile(r"Active:\s(.*)\n")
    __DESCRIPTION_PATTERN = re.compile(
        r"(^\s+Loaded:\s.*\n|^\s+Process:\s.*\n|^\s+Main PID:\s.*\n|^\s+CGroup:\s.*(\n.*)+\n\n)",
        re.MULTILINE
    )

    @staticmethod
    def __exec(cmd):
        return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()[0].decode('utf-8')

    def start_service(self, service_name):
        return self.__exec(SYSTEMCTL_COMMANDS.START.format(service_name))

    def restart_service(self, service_name):
        return self.__exec(SYSTEMCTL_COMMANDS.RESTART.format(service_name))

    def stop_service(self, service_name):
        return self.__exec(SYSTEMCTL_COMMANDS.STOP.format(service_name))

    def get_service_status(self, service):
        status = self.__exec(SYSTEMCTL_COMMANDS.STATUS.format(service))
        if status:
            name = re.findall(self.__NAME_PATTERN, status)
            service_name = re.findall(self.__SERVICE_NAME_PATTERN, status)[0]
            return {
                'name': name[0] if name else service_name,
                'service_name': service_name,
                'status': re.findall(self.__STATUS_PATTERN, status)[0],
                'description': ''.join(map(lambda x: x[0], re.findall(self.__DESCRIPTION_PATTERN, status)))
            }
        return None

    def __extract_data(self, services_name):
        return list(sorted(filter(bool, map(self.get_service_status, services_name)), key=operator.itemgetter('name')))

    def get_enabled_services(self):
        return self.__extract_data(self.__exec(SYSTEMCTL_COMMANDS.ENABLED_SERVICES).split('\n')[:-1:])

    def get_active_services(self):
        return self.__extract_data(re.findall(self.__SERVICE_PATTERN, self.__exec(SYSTEMCTL_COMMANDS.STATUS_ALL)))

    def get_failed_services(self):
        return self.__exec(SYSTEMCTL_COMMANDS.FAILED_SERVICES)


if __name__ == '__main__':
    monitor = ServiceMonitor()
    print(monitor.get_service_status('mysql'))
    print(monitor.get_active_services())
    print(monitor.get_enabled_services())
    print(monitor.get_failed_services())
