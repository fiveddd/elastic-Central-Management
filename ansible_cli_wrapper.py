#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time    : 2019/6/26 4:01 PM
# @Author  : lij021
# @File    : ansible_cli_wrapper.py

import ansible
from ansible.cli.playbook import PlaybookCLI
from ansible.plugins.callback import CallbackBase
import json
from ansible.cli import CLI
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible import context
from ansible.utils.context_objects import CLIArgs
from ansible import constants as C
from logging import getLogger
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from optparse import Values
import time

logger = getLogger('ansible_wrapper')

INVENTORY_PATH = './inventory/'


# 因为ansible module里面的代码使用了immutableDict，导致参数不能二次初始化，即不能运行多次，需要修改这部分代码
def _init_global_context(cli_args):
    """Initialize the global context objects"""
    context.CLIARGS = CLIArgs.from_options(cli_args)


context._init_global_context = _init_global_context


def create_task():
    return {
        'id': int(time.time() * 10000),
        'message': [],
        'status': 'start'

    }


class ResultCallback(CallbackBase):
    def __init__(self, result_buffer):
        super().__init__()
        self.result_buffer = result_buffer
        self.template = '''<div class="ivu-tabs-content ivu-tabs-content-animated";">
    <div class="ivu-card">
        <div class="ivu-card-head"><p slot="title" style="color: %s">%s: %s</p></div>
        <div class="ivu-card-body">
            <span>%s</span>
        </div>
    </div>
</div>'''

    def v2_runner_on_ok(self, result, **kwargs):
        host = result._host
        print('===v2_runner_on_ok====host=%s===result=%s' % (host, result._result))
        self.result_buffer['message'].append(self.template % ('#19be6b', str(host), 'ok', result._result))

    def v2_runner_on_failed(self, result, **kwargs):
        host = result._host.get_name()
        self.runner_on_failed(host, result._result, False)
        print('===v2_runner_on_failed====host=%s===result=%s' % (host, result._result))
        content = self.template % ('#ed4014', str(host), 'failed', result._result)
        print(content)
        self.result_buffer['message'].append(content)

    def v2_runner_on_unreachable(self, result):
        host = result._host.get_name()
        self.runner_on_unreachable(host, result._result)
        self.result_buffer['message'].append(self.template % ('#c5c8ce', str(host), 'unreachable', result._result))

    def v2_runner_on_skipped(self, result):
        host = result._host.get_name()
        self.runner_on_skipped(host, self._get_item(getattr(result._result, 'results', {})))
        self.result_buffer['message'].append(self.template % ('#c5c8ce', str(host), 'skip', result._result))

    def v2_playbook_on_stats(self, stats):
        self.result_buffer['status'] = 'done'
        print('===========play executes completed========')


def runansible(task, inventory, host_list, task_list, remote_user=None, become_user=None):
    options = {'verbosity': 0, 'ask_pass': False, 'private_key_file': None, 'remote_user': remote_user,
               'connection': 'smart', 'timeout': 30, 'ssh_common_args': '', 'sftp_extra_args': '',
               'scp_extra_args': '', 'ssh_extra_args': '', 'force_handlers': False, 'flush_cache': None,
               'become': False, 'become_method': 'sudo', 'become_user': become_user, 'become_ask_pass': False,
               'check': False, 'syntax': None, 'diff': False,
               'inventory': inventory, 'verbosity': None, 'check': None}

    loader = DataLoader()
    passwords = dict()
    results_callback = ResultCallback(task)
    inventory = InventoryManager(loader=loader, sources=[options['inventory']])
    variable_manager = VariableManager(loader=loader, inventory=inventory)
    play_source = dict(
            name="Python play Ansible",
            hosts=host_list,
            gather_facts='no',
            become_method='sudo',
            become_user=become_user,
            tasks=task_list
    )
    play = Play().load(play_source, variable_manager=variable_manager, loader=loader)

    tqm = None
    try:
        tqm = TaskQueueManager(
                inventory=inventory,
                variable_manager=variable_manager,
                loader=loader,
                passwords=passwords,
                stdout_callback=results_callback,
                run_additional_callbacks=C.DEFAULT_LOAD_CALLBACK_PLUGINS,
                run_tree=False,
        )
        return tqm.run(play)
    finally:
        if tqm is not None:
            tqm.cleanup()


def run_playbook(task, inventory='hosts_dev', play_book='fetch_config.yml'):
    try:
        cli = PlaybookCLI([" ", '-i', INVENTORY_PATH + inventory, play_book])

        super(PlaybookCLI, cli).run()

        loader, inventory, variable_manager = cli._play_prereqs()

        CLI.get_host_list(inventory, context.CLIARGS['subset'])

        pbex = PlaybookExecutor(playbooks=context.CLIARGS['args'], inventory=inventory,
                                variable_manager=variable_manager, loader=loader,
                                passwords=None)

        pbex._tqm._stdout_callback = ResultCallback(task)
        pbex.run()
        return True
    except Exception as e:
        logger.error(e)
        return False


def pb_get_inventory(host_file='hosts_dev', type=None):
    try:
        loader = DataLoader()
        inventory = InventoryManager(loader=loader, sources=[INVENTORY_PATH + host_file])
        groups = inventory.groups
        result = {}
        for key in groups.keys():
            if len(groups[key].hosts):
                group = []
                for h in groups[key].hosts:
                    group.append({
                        "name": h.name,
                        "ip": h.vars['ansible_host'],
                        "user": h.vars['ansible_user'],
                    })
                if type in key:
                    result[key] = group
        return result
    except Exception as e:
        logger.error(e)
        return None


def play_get_etc_config(task, inventory, host, type):
    config_path = '/etc/{}/{}.yml'.format(type, type)
    tasks_list = [
        dict(action=dict(module='fetch',
                         args='src=%s dest=./tmp/%s-{{ inventory_hostname }} flat=yes' % (config_path, type))),
    ]
    return runansible(task, INVENTORY_PATH + inventory, [host], tasks_list)


def play_upload_etc_config(task, inventory, host, type, content):
    config_path = '/etc/{}/{}.yml'.format(type, type)
    file_path = './tmp/%s-%s' % (type, host)
    with open(file_path, 'wb') as f:
        f.write(content)
    tasks_list = [
        dict(action=dict(module='copy',
                         args='src=%s dest=%s owner=%s group=%s mode=0644' % (file_path, config_path, type, type))),
    ]
    return runansible(task, INVENTORY_PATH + inventory, [host], tasks_list, remote_user='jboss', become_user=type)

def pb_upload_reset_config(task, inventory, host, type, content):
    config_path = '/etc/{}/{}.yml'.format(type, type)
    file_path = './tmp/%s-%s' % (type, host)
    with open(file_path, 'wb') as f:
        f.write(content)
    with open('./playbook_template/upload_and_restart.yml', 'r') as t:
        template = t.read()
    with open('./upload_and_restart.yml', 'w') as pb:
        pb_content = template % (host, file_path, config_path, type)
        print(pb_content)
        pb.write(pb_content)
    return run_playbook(task, inventory, 'upload_and_restart.yml')

if __name__ == '__main__':
    play_get_etc_config(create_task(), 'hosts.uat', 'kibana_all', 'kibana')
