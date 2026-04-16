import ctypes
import getpass
import os
import sys
import time

from win32com import client
from xml.etree import ElementTree as ET

from loguru import logger


class AutostartService:

    register_key: str = 'WTRPC'
    target_file: str = 'WTDRP.exe'

    @staticmethod
    def get_user_is_admin() -> bool:
        logger.info('Checking user is admin')
        try:
            data = ctypes.windll.shell32.IsUserAnAdmin()
            logger.info(f'Check result -> {data}')
            return data
        except Exception as e:
            logger.error(e)
            return False

    @logger.catch
    def __create_schedule_xml(self) -> str:
        task = ET.Element(
            'Task', attrib={
                'version': '1.2',
                'xmlns': 'http://schemas.microsoft.com/windows/2004/02/mit/task' # noqa
            }
        )

        current_user = getpass.getuser()

        logger.debug(f'XML schedule user -> {current_user}')
        logger.debug(f'App registration name -> {self.register_key}')

        register_date = '2026-04-16T19:07:52.1706939'
        desc = 'Autostart job for War Thunder discord rich presence'

        registration_info = ET.SubElement(task, 'RegistrationInfo')
        ET.SubElement(registration_info, 'Date').text = register_date
        ET.SubElement(registration_info, 'Author').text = current_user
        ET.SubElement(registration_info, 'Description').text = desc
        ET.SubElement(registration_info, 'URI').text = f'\\{self.register_key}' # noqa

        triggers = ET.SubElement(task, 'Triggers')
        logon_trigger = ET.SubElement(triggers, 'LogonTrigger')
        ET.SubElement(logon_trigger, 'Enabled').text = 'true'
        ET.SubElement(logon_trigger, 'UserId').text = current_user

        principals = ET.SubElement(task, 'Principals')
        principal = ET.SubElement(
            principals, 'Principal', attrib={'id': 'Author'}
            )
        ET.SubElement(principal, 'LogonType').text = 'InteractiveToken'
        ET.SubElement(principal, 'RunLevel').text = 'LeastPrivilege'

        settings = ET.SubElement(task, 'Settings')
        ET.SubElement(settings, 'MultipleInstancesPolicy').text = 'IgnoreNew'
        ET.SubElement(settings, 'DisallowStartIfOnBatteries').text = 'false'
        ET.SubElement(settings, 'StopIfGoingOnBatteries').text = 'true'
        ET.SubElement(settings, 'AllowHardTerminate').text = 'true'
        ET.SubElement(settings, 'StartWhenAvailable').text = 'false'
        ET.SubElement(settings, 'RunOnlyIfNetworkAvailable').text = 'false'
        idle_settings = ET.SubElement(settings, 'IdleSettings')
        ET.SubElement(idle_settings, 'StopOnIdleEnd').text = 'true'
        ET.SubElement(idle_settings, 'RestartOnIdle').text = 'false'
        ET.SubElement(settings, 'AllowStartOnDemand').text = 'true'
        ET.SubElement(settings, 'Enabled').text = 'true'
        ET.SubElement(settings, 'Hidden').text = 'false'
        ET.SubElement(settings, 'RunOnlyIfIdle').text = 'false'
        ET.SubElement(settings, 'WakeToRun').text = 'false'
        ET.SubElement(settings, 'ExecutionTimeLimit').text = 'PT0S'
        ET.SubElement(settings, 'Priority').text = '7'
        restart_on_failure = ET.SubElement(settings, 'RestartOnFailure')
        ET.SubElement(restart_on_failure, 'Interval').text = 'PT1M'
        ET.SubElement(restart_on_failure, 'Count').text = '3'

        app_path = fr'{os.getcwd()}\{self.target_file}'
        logger.debug(f'App path -> {app_path}')
        actions = ET.SubElement(task, 'Actions', attrib={'Context': 'Author'})
        exec_elem = ET.SubElement(actions, 'Exec')
        ET.SubElement(exec_elem, 'Command').text = app_path
        ET.SubElement(exec_elem, 'WorkingDirectory').text = os.getcwd()

        tree = ET.ElementTree(task)
        xml_name = 'task.xml'
        tree.write('task.xml', encoding='utf-16', xml_declaration=True)
        logger.debug('Xml task description created')
        return xml_name

    def add_to_scheduler(self) -> None:
        logger.info('Adding task to scheduler')
        xml_path = self.__create_schedule_xml()
        cmd = f'schtasks /Create /XML {xml_path} /TN {self.register_key} /F'
        logger.debug(f'Add task command -> {cmd}')
        os.system(cmd)
        logger.info('Task added to scheduler')
        os.remove('task.xml')

    @logger.catch
    def delete_startup(self):
        logger.info('Deleting Register Key')
        scheduler = client.Dispatch("Schedule.Service")
        scheduler.Connect()
        try:
            scheduler.GetFolder("\\").DeleteTask(self.register_key, 0)
            logger.info(f'Task -> {self.register_key} deleted!')
        except Exception as e:
            logger.error(e)


if __name__ == '__main__':
    logger.add('autostart_service.log', level='DEBUG')
    input_vars = ('add', 'delete', 'exit', 'a', 'd', 'e')
    user_input = input(f'Enter a command {input_vars}: ')
    logger.debug(f'user command: {user_input}')
    while user_input not in input_vars:
        logger.warning(f'Invalid command: {user_input}')
        time.sleep(2)
        user_input = input(f'Enter a command {input_vars}: ')
    autostart_service = AutostartService()
    user_is_admin = autostart_service.get_user_is_admin()
    if user_is_admin:
        logger.info('User is admin')
        if user_input in input_vars:
            if user_input == 'add' or user_input == 'a':
                autostart_service.add_to_scheduler()
            elif user_input == 'delete' or user_input == 'd':
                autostart_service.delete_startup()
            elif user_input == 'exit' or user_input == 'e':
                sys.exit()
    else:
        logger.warning('User is not admin')
        input('Press any key to exit')
        sys.exit()
