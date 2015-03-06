# -*-  coding: utf-8 -*-
""""""
# -
# Copyright (C) 2015 ZetaOps Inc.
#
# This file is licensed under the GNU General Public License v3
# (GPLv3).  See LICENSE.txt for details.
from SpiffWorkflow import Task
from SpiffWorkflow.bpmn.BpmnWorkflow import BpmnWorkflow
from tests.SpiffWorkflow.pytests.testengine import BpmnTestEngine

__author__ = "Evren Esat Ozkan"


# def tessssssst_dummy():
#     we = BpmnTestEngine('Message Interrupts SP')
#
#     we.save_restore()
#
#     we.workflow.do_engine_steps()
#     we.save_restore()
#
#     assert 1 == len(we.workflow.get_tasks(Task.READY))
#     assert 1 == len(we.workflow.get_tasks(Task.WAITING))
#
#     we.do_next_exclusive_step('Do Something In a Subprocess')
#     we.workflow.do_engine_steps()
#     we.save_restore()
#
#     we.do_next_exclusive_step('Ack Subprocess Done')
#     we.workflow.do_engine_steps()
#
#     we.save_restore()
#
#     we.workflow.do_engine_steps()
#
#     assert 0 == len(we.workflow.get_tasks(Task.READY | Task.WAITING))

def test_subprocess_with_usertask():
    we = BpmnTestEngine('main_proccess_id', 'subprocess.bpmn')
    we.save_restore()
    we.workflow.do_engine_steps()
    we.save_restore()
    we.do_next_exclusive_step('Do Something')
    we.save_restore()
    we.workflow.do_engine_steps()
    print we.workflow.task_tree.get_dump()
    assert 0 == len(we.workflow.get_tasks(Task.READY | Task.WAITING))
