
"""Create configuration to deploy GKE cluster."""

OAUTH_DEFAULT = [
    'https://www.googleapis.com/auth/compute',
    'https://www.googleapis.com/auth/devstorage.read_only',
    'https://www.googleapis.com/auth/logging.write',
    'https://www.googleapis.com/auth/monitoring',
    'https://www.googleapis.com/auth/servicecontrol',
    'https://www.googleapis.com/auth/service.management.readonly',
    'https://www.googleapis.com/auth/trace.append'
]

DEFAULT_NODE_POOL = [{
    'name': 'default-inside-cluster',
    'config': {
        'machineType': 'f1-micro', #set the machine type
        'oauthScopes': OAUTH_DEFAULT,
        'preemptible': True,
        'taints': [
            {
                'effect': 'NO_SCHEDULE',
                'key': 'default_node',
                'value': 'true'
            }
        ],
    },
    'initialNodeCount': 2,
    'version': '1.8.10-gke.0', #set the gke version
    'autoscaling': {
        'enabled': False
    },
    'management': {
      'autoRepair': True,
      'autoUpgrade': False
    }
}]


def GenerateSubnetwork(context):
    """In case if there's no ip allocation policy enabled for the cluster object
    google API requires to define subnetwork on the top level of the object's properties
    otherwise it has to be omitted or set to empty string"""

    if context.properties['ipAllocationPolicy']['createSubnetwork']:
        return ''
    return context.properties['subnetwork']

def GenerateNodePoolDMobject(node_pool, cluster_name, project, region, obj_type):
    """Generate nodePool DM object"""

    node_pool_config = {
                      'type': obj_type,
                      'name': node_pool['name'],
                      'properties': {
                          'clusterId': cluster_name,
                          'parent': 'projects/{}/locations/{}/clusters/{}'.format(project, region, cluster_name),
                          'nodePool': node_pool
                          }
                      }

    return node_pool_config


def GenerateConfig(context):
  """Generate YAML resource configuration."""

  cluster_name = context.env['deployment'] + '-' + context.env['name']

  resources = []
  cluster = {
      'name': cluster_name,
      'type': context.properties['cluster_type'],
      'properties': {
          'parent': "projects/{}/locations/{}".format(context.env['project'], context.properties['region']),
          'cluster': {
              'name': cluster_name,
              'initialClusterVersion': context.properties['initialClusterVersion'],
              'nodePools': DEFAULT_NODE_POOL,
              'network': context.properties['network'],
              'subnetwork': GenerateSubnetwork(context),
              'legacyAbac': context.properties['legacyAbac'],
              'addonsConfig': context.properties['addonsConfig'],
              'networkPolicy': context.properties['networkPolicy'],
              'ipAllocationPolicy': context.properties['ipAllocationPolicy']
          }
      }
  }
  resources.append(cluster)

  for node_pool in context.properties.get('nodePools', []):
      resources.append(
          GenerateNodePoolDMobject(
              node_pool,
              "$(ref.{}.name)".format(cluster_name),
              context.env['project'],
              context.properties['region'],
              context.properties['node_pool_type']
          )
      )

  outputs = []
  return {'resources': resources, 'outputs': outputs}
