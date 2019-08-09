import operator
import re
import subprocess


class SystemctlCommands:
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

    @classmethod
    def start_service(cls, service_name):
        return cls.__exec(SystemctlCommands.START.format(service_name))

    @classmethod
    def restart_service(cls, service_name):
        return cls.__exec(SystemctlCommands.RESTART.format(service_name))

    @classmethod
    def stop_service(cls, service_name):
        return cls.__exec(SystemctlCommands.STOP.format(service_name))

    @classmethod
    def get_service_status(cls, service):
        status = cls.__exec(SystemctlCommands.STATUS.format(service))
        if status:
            name = re.findall(cls.__NAME_PATTERN, status)
            service_name = re.findall(cls.__SERVICE_NAME_PATTERN, status)[0]
            return {
                'name': name[0] if name else service_name,
                'service_name': service_name,
                'status': re.findall(cls.__STATUS_PATTERN, status)[0],
                'description': ''.join(map(lambda x: x[0], re.findall(cls.__DESCRIPTION_PATTERN, status)))
            }
        return None

    @classmethod
    def __extract_data(cls, service_names):
        service_info_map = {x['name']: x for x in filter(bool, map(cls.get_service_status, service_names))}
        return list(sorted(service_info_map.values(), key=operator.itemgetter('name')))

    @classmethod
    def get_enabled_services(cls):
        return cls.__extract_data(cls.__exec(SystemctlCommands.ENABLED_SERVICES).split('\n')[:-1:])

    @classmethod
    def get_active_services(cls):
        return cls.__extract_data(re.findall(cls.__SERVICE_PATTERN, cls.__exec(SystemctlCommands.STATUS_ALL)))

    @classmethod
    def get_inactive_services(cls):
        return list(filter(lambda x: 'inactive' in x['status'], cls.get_enabled_services()))

    @classmethod
    def get_failed_services(cls):
        return cls.__exec(SystemctlCommands.FAILED_SERVICES)


if __name__ == '__main__':
    monitor = ServiceMonitor()
    print(monitor.get_service_status('mysql'))
    print(monitor.get_active_services())
    print(monitor.get_inactive_services())
    print(monitor.get_enabled_services())
    print(monitor.get_failed_services())
