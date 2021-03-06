# -*- coding: utf-8 -*- #
# Copyright 2019 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Command for listing existing triggers."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.events import eventflow_operations
from googlecloudsdk.command_lib.events import exceptions
from googlecloudsdk.command_lib.run import connection_context
from googlecloudsdk.command_lib.run import flags
from googlecloudsdk.command_lib.run import resource_args
from googlecloudsdk.command_lib.util.concepts import concept_parsers


class List(base.ListCommand):
  """List available event types categories."""

  detailed_help = {
      'DESCRIPTION': """\
          {description}
          """,
      'EXAMPLES': """\
          To list available event type categories:

              $ {command}
          """,
  }

  @staticmethod
  def CommonArgs(parser):
    # Flags specific to managed CR
    managed_group = flags.GetManagedArgGroup(parser)
    concept_parsers.ConceptParser([
        resource_args.CLOUD_RUN_LOCATION_PRESENTATION
    ]).AddToParser(managed_group)
    # Flags specific to CRoGKE
    gke_group = flags.GetGkeArgGroup(parser)
    concept_parsers.ConceptParser(
        [resource_args.CLUSTER_PRESENTATION]).AddToParser(gke_group)
    # Flags specific to connecting to a Kubernetes cluster (kubeconfig)
    kubernetes_group = flags.GetKubernetesArgGroup(parser)
    flags.AddKubeconfigFlags(kubernetes_group)
    # Flags not specific to any platform
    flags.AddPlatformArg(parser)
    parser.display_info.AddFormat("""table(
        source_kind:label=CATEGORY:sort=1)""")

  @staticmethod
  def Args(parser):
    List.CommonArgs(parser)

  def Run(self, args):
    conn_context = connection_context.GetConnectionContext(args)
    if conn_context.supports_one_platform:
      raise exceptions.UnsupportedArgumentError(
          'Events are only available with Cloud Run for Anthos.')

    with eventflow_operations.Connect(conn_context) as client:
      source_crds = client.ListSourceCustomResourceDefinitions()
      return [crd for crd in source_crds if crd.event_types]
