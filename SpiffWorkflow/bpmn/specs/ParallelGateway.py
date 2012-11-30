# Copyright (C) 2012 Matthew Hampton
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
from collections import deque

import logging
from SpiffWorkflow.Task import Task
from SpiffWorkflow.bpmn.specs.UnstructuredJoin import UnstructuredJoin

LOG = logging.getLogger(__name__)

class ParallelGateway(UnstructuredJoin):
    """
    Task Spec for a bpmn:parallelGateway node.
    From the specification of BPMN (http://www.omg.org/spec/BPMN/2.0/PDF - document number:formal/2011-01-03):
        The Parallel Gateway is activated if there is at least one token on each incoming Sequence Flow.
        The Parallel Gateway consumes exactly one token from each incoming
        Sequence Flow and produces exactly one token at each outgoing Sequence Flow.

        TODO: Not implemented:
        If there are excess tokens at an incoming Sequence Flow, these tokens
        remain at this Sequence Flow after execution of the Gateway.

    Essentially, this means that we must wait until we have a completed parent task on each incoming sequence.

    """

    def _try_fire_unstructured(self, my_task, force=False):
        # Look at the tree to find all places where this task is used.
        tasks = []
        for task in my_task.workflow.task_tree:
            if task.thread_id != my_task.thread_id:
                continue
            if task.workflow != my_task.workflow:
                continue
            if task.task_spec != self:
                continue
            if task._is_finished():
                continue
            tasks.append(task)

        # Look up which tasks have parent's completed.
        waiting_tasks = []
        completed_inputs = set()
        for task in tasks:
            if task.parent._has_state(Task.COMPLETED) and (task._has_state(Task.WAITING) or task == my_task):
                if task.parent.task_spec in completed_inputs:
                    raise NotImplementedError("Unsupported looping behaviour: two threads waiting on the same sequence flow.")
                completed_inputs.add(task.parent.task_spec)
            else:
                waiting_tasks.append(task.parent)

        # If the threshold was reached, get ready to fire.
        return force or len(completed_inputs) >= len(self.inputs), waiting_tasks
