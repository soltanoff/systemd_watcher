import operator

import dbus


def catch_dbus_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except dbus.exceptions.DBusException as error:
            print(error)
            return None

    return wrapper


class ServiceMonitor(object):

    BUS_NAME = "org.freedesktop.systemd1"
    OBJECT_PATH = "/org/freedesktop/systemd1"

    DBUS_MANAGER_INTERFACE = "org.freedesktop.systemd1.Manager"
    DBUS_PROPERTIES_INTERFACE = "org.freedesktop.DBus.Properties"

    UNIT_INTERFACE = "org.freedesktop.systemd1.Unit"
    SERVICE_UNIT_INTERFACE = "org.freedesktop.systemd1.Service"

    __instance = None

    def __init__(self):
        self.__bus = dbus.SystemBus()

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(ServiceMonitor, cls).__new__(cls)
        return cls.__instance

    @property
    def _interface(self):
        return dbus.Interface(self.__bus.get_object(self.BUS_NAME, self.OBJECT_PATH), self.DBUS_MANAGER_INTERFACE)

    def _get_unit_properties_by_interface(self, unit_name, unit_interface):
        obj = self.__bus.get_object(self.BUS_NAME, self._interface.LoadUnit(unit_name))
        properties_interface = dbus.Interface(obj, self.DBUS_PROPERTIES_INTERFACE)
        return properties_interface.GetAll(unit_interface)

    def _iter_services(self, status=None):
        for dbus_service_info in self._interface.ListUnits():
            service_name = dbus_service_info[0]
            service_status = dbus_service_info[3]
            service_active_stage = dbus_service_info[4]
            if (status is None or status == service_status) \
                    and '.service' in service_name \
                    and '@' not in service_name \
                    and not service_name.startswith('systemd') \
                    and service_active_stage != 'exited':
                yield self.get_service_status(service_name)

    @catch_dbus_exception
    def start_service(self, service_name, mode="replace"):
        self._interface.StartUnit(service_name, mode)

    @catch_dbus_exception
    def restart_service(self, service_name, mode="replace"):
        self._interface.RestartUnit(service_name, mode)

    @catch_dbus_exception
    def stop_service(self, service_name, mode="replace"):
        self._interface.StopUnit(service_name, mode)

    @catch_dbus_exception
    def get_service_status(self, service_name):
        service_property = self._get_unit_properties_by_interface(service_name, self.SERVICE_UNIT_INTERFACE)
        unit_property = self._get_unit_properties_by_interface(service_name, self.UNIT_INTERFACE)

        unit_file_state = unit_property.get('UnitFilePreset')
        service_name = str(unit_property['Id'])
        description = str(unit_property['Description'])
        status = "{activeState} ({subState})".format(
            activeState=unit_property['ActiveState'],
            subState=unit_property['SubState'],
        )
        service_info = "● {id} - {description}\n" \
                       "Loaded: {loadState} ({fragmentPath}; {unitFileState}; vendor preset; {unitFilePreset})\n" \
                       "Active: {status}\n" \
                       "Main PID: {pid}\n" \
                       "Tasks: {tasksCurrent}\n" \
                       "Memory: {memoryCurrent}M\n" \
                       "CPU: {CPUUsageNSec}s\n" \
                       "CGroup: {controlGroup}\n".format(
            id=service_name,
            description=description,
            loadState=unit_property['LoadState'],
            fragmentPath=unit_property['FragmentPath'],
            unitFileState=unit_property['UnitFileState'],
            unitFilePreset=unit_property['UnitFilePreset'],
            status=status,
            pid=service_property['MainPID'],
            tasksCurrent=service_property['TasksCurrent'],
            memoryCurrent=service_property['MemoryCurrent'] / 1024.0 / 1024.0,
            CPUUsageNSec=service_property['CPUUsageNSec'] / 1000000.0,
            controlGroup=service_property['ControlGroup'],
        )

        exec_start = service_property['ExecStart']
        if exec_start:
            service_info += "Exec start: {0}\n".format(' '.join(exec_start[0][1]))

        exec_start_post = service_property['ExecStartPost']
        if exec_start_post:
            service_info += "Exec start post: {0}\n".format(' '.join(exec_start_post[0][1]))

        exec_start_pre = service_property['ExecStartPre']
        if exec_start_pre:
            service_info += "Exec start pre: {0}\n".format(' '.join(exec_start_pre[0][1]))

        exec_stop = service_property['ExecStop']
        if exec_stop:
            service_info += "Exec stop: {0}\n".format(' '.join(exec_stop[0][1]))

        failure_action = service_property['FailureAction']
        if failure_action:
            service_info += "Failure action: {0}\n".format(failure_action)

        exec_main_status = service_property['ExecMainStatus']
        if exec_main_status:
            service_info += "Exec main status: {0}\n".format(exec_main_status)

        return {
            'name': description if description else service_name,
            'service_name': service_name,
            'status': status,
            'unit_file_state': str(unit_file_state) if unit_file_state else None,
            'description': service_info,
        }

    @catch_dbus_exception
    def get_enabled_services(self):
        return list(sorted(self._iter_services(), key=operator.itemgetter('name')))

    @catch_dbus_exception
    def get_active_services(self):
        return list(sorted(self._iter_services(status='active'), key=operator.itemgetter('name')))

    @catch_dbus_exception
    def get_inactive_services(self):
        return list(sorted(self._iter_services(status='inactive'), key=operator.itemgetter('name')))

    @catch_dbus_exception
    def get_failed_services(self):
        return list(sorted(self._iter_services(status='failed'), key=operator.itemgetter('name')))


if __name__ == '__main__':
    monitor = ServiceMonitor()
    print(monitor.get_service_status('mysql.service'))
    print(monitor.get_active_services())
    print(monitor.get_inactive_services())
    print(monitor.get_enabled_services())
    print(monitor.get_failed_services())
