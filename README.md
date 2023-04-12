# DuploCloud Pipelines Pipe: Deploy  

Updates a lambdas image tag on DuploCloud. 

## YAML Definition  

```yaml
- pipe: docker://duplocloud/bitbucket-lambda-deploy-pipe:1.0.0
  variables:
    DUPLO_TOKEN: '<string>'
    DUPLO_HOST: '<string>'
    TENANT: '<string>'
    LAMBDAS: '<string>'
    IMAGE: '<string>'
```

## Variables  

| Variable | Usage |  
| -------- | ----- |  
| DUPLO_TOKEN | Auth token for Duplo |  
| DUPLO_HOST | The domain of your Duplo instance |  
| TENANT | The tenant where the lambda is in |  
| LAMBDAS | The comma separated names of the lambdas to update |  
| IMAGE | The new image of the lambda. | 

## Prerequisites  

To make an update to a lambda you will need a duplo token. 