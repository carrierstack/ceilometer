#
# Copyright 2012 eNovance <licensing@enovance.com>
# Copyright 2012 Red Hat, Inc
#
# Author: Julien Danjou <julien@danjou.info>
# Author: Eoghan Glynn <eglynn@redhat.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import mock

from ceilometer.compute import manager
from ceilometer.compute.pollsters import instance as pollsters_instance
from ceilometer.tests.compute.pollsters import base


class TestInstancePollster(base.TestPollsterBase):

    def setUp(self):
        super(TestInstancePollster, self).setUp()

    @mock.patch('ceilometer.pipeline.setup_pipeline', mock.MagicMock())
    def test_get_samples_instance(self):
        mgr = manager.AgentManager()
        pollster = pollsters_instance.InstancePollster()
        samples = list(pollster.get_samples(mgr, {}, [self.instance]))
        self.assertEqual(1, len(samples))
        self.assertEqual('instance', samples[0].name)
        self.assertEqual(1, samples[0].resource_metadata['vcpus'])
        self.assertEqual(512, samples[0].resource_metadata['memory_mb'])
        self.assertEqual(20, samples[0].resource_metadata['disk_gb'])
        self.assertEqual(20, samples[0].resource_metadata['root_gb'])
        self.assertEqual(0, samples[0].resource_metadata['ephemeral_gb'])
        self.assertEqual('active', samples[0].resource_metadata['status'])

    @mock.patch('ceilometer.pipeline.setup_pipeline', mock.MagicMock())
    def test_get_samples_instance_flavor(self):
        mgr = manager.AgentManager()
        pollster = pollsters_instance.InstanceFlavorPollster()
        samples = list(pollster.get_samples(mgr, {}, [self.instance]))
        self.assertEqual(1, len(samples))
        self.assertEqual('instance:m1.small', samples[0].name)
