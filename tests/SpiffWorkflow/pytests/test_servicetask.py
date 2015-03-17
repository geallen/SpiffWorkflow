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


def test_servicetask_with_class():
    we = BpmnTestEngine('Process_1', 'servicetask_class.bpmn')
    we.get_named_step('StartEvent_1').complete()
    we.full_save_restore()
    we.save_restore()
    service_task = we.get_named_step('ServiceTask_class')
    assert 'views.module.ViewClass' == service_task.task_spec.service_class
    # we.save_restore()
    we.workflow.do_engine_steps()
    # print we.workflow.task_tree.get_dump()
    assert 0 == len(we.workflow.get_tasks(Task.READY | Task.WAITING))


def test_servicetask_with_expression():
    we = BpmnTestEngine('Process_1', 'servicetask_expression.bpmn')
    we.get_named_step('StartEvent_1').complete()
    we.full_save_restore()
    we.save_restore()
    service_task = we.get_named_step('ServiceTask_expression')
    assert 'views.module.method' == service_task.task_spec.expression
    assert 'result_variable_name' == service_task.task_spec.result_variable
    # we.save_restore()
    we.workflow.do_engine_steps()
    # print we.workflow.task_tree.get_dump()
    assert 0 == len(we.workflow.get_tasks(Task.READY | Task.WAITING))
