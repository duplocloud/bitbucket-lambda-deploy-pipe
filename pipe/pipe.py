import requests
from bitbucket_pipes_toolkit import Pipe, yaml, get_variable, get_logger

# some global vars
REQUESTS_DEFAULT_TIMEOUT = 10

# Required vars for updating a lambda
schema = {
  'DUPLO_TOKEN': {'required': True, 'type': 'string'},
  'DUPLO_HOST': {'required': True, 'type': 'string'},
  'TENANT': {'required': True, 'type': 'string'},
  'LAMBDAS': {'required': True, 'type': 'string'},
  'IMAGE': {'required': True, 'type': 'string'}
}

logger = get_logger()

class DuploDeploy(Pipe):
  """Duplo Deploy Pipe"""
  url = None
  headers = None
  lambdas = None
  image = None
  tenant_name = None
  tenant_id = None

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    token = self.get_variable("DUPLO_TOKEN")
    self.url = self.get_variable("DUPLO_HOST")
    self.lambdas = self.get_variable("LAMBDAS")
    self.tenant_name = self.get_variable("TENANT")
    self.image = self.get_variable("IMAGE")
    self.headers = {
      'Content-Type': 'application/json',
      'Authorization': f"Bearer {token}"
    }
  
  def get_tenant_id(self):
    """Get Tenant ID
    Retrieves the tennats ID based on the name variable.
    """
    try:
      response = requests.get(
        url=f"{self.url}/adminproxy/GetTenantNames",
        headers=self.headers,
        timeout=REQUESTS_DEFAULT_TIMEOUT
      )
      tenant = [t for t in response.json() if t["AccountName"] == self.tenant_name][0]
      return tenant["TenantId"]
    except Exception as e:
      self.fail(f"Could find tenant named {self.tenant_name}")

  def update_image(self, lambda_name):
    try:
      tenant_id = self.get_tenant_id()
      data = {
        "FunctionName": lambda_name,
        "ImageUri": self.image
      }
      response = requests.post(
        url=f"{self.url}/subscriptions/{tenant_id}/UpdateLambdaFunction",
        headers=self.headers,
        json=data,
        timeout=REQUESTS_DEFAULT_TIMEOUT
      )
      if 200 <= response.status_code <= 299:
          self.success(f"Updated {lambda_name} image to {self.image}")
      else:
          self.fail(f"Unable to update {lambda_name} image to {self.image}")
    except requests.exceptions.Timeout as error:
      self.fail(error)
    except requests.ConnectionError as error:
      self.fail(error)

  def run(self):
    super().run()
    self.tenant_id = self.get_tenant_id()

    lambdas = self.lambdas.split(',')
    for lambda_name in lambdas:
        logger.info(f"Updating {lambda_name} in {self.tenant_name}")
        self.update_image(lambda_name)

if __name__ == '__main__':
  with open('/pipe.yml', 'r') as metadata_file:
    metadata = yaml.safe_load(metadata_file.read())
  duplo_deploy = DuploDeploy(pipe_metadata=metadata, schema=schema)
  duplo_deploy.run()