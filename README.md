# [Azure Durable Functions](https://docs.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-overview) : Extract frames/images from Video

This application uses Azure Durable functions, Blob Storage, Event Grid and OpenCV-Python

## Create Storage Account
Open [Azure Cloud Shell](https://shell.azure.com) and run below commands

```bash
az storage account create \
  --name <account-name> \
  --resource-group <resource-group-name> \
  --location westus \
  --sku Standard_RAGRS \
  --kind StorageV2
```
### Crate Blob Containers
```bash
# Create container named "uploads", this is where you will post your video files

az storage container create --name uploads --accountname <storage account name from above step>

# Create container named "images", this is where Functions app will extract and uploads images 
az storage container create --name images --accountname <storage account name from above step>
```

## Deploy Function App
To deploy the functions application code please follow [these](https://docs.microsoft.com/en-us/azure/azure-functions/functions-continuous-deployment) steps Or use [VS Code](https://code.visualstudio.com/tutorials/functions-extension/deploy-app) to deploy the application.

Once the app is deployed, add ACCOUNT_NAME and ACCOUNT_KEY  in application settings in Configuration for your storage account created above

## Create Event Grid Subscription
In this application Event Grid is used to trigger the functions app when a new Video is added to videos blob containers. 
Before we create event grid subscription we need to get system key. Replace code= with your master key.
https://```<function-app-name>```.azurewebsites.net/admin/host/systemkeys/eventgrid_extension?```code=<master-key>```
 
This should result in something like below.
```json
{"name": "eventgrid_extension",
"value": "2aSighjJgTUxhaOaCBN91QA0y5celLfFP1WOKzTasdfdf2THig==",
"links": [{
"rel": "self",
"href": "https://<function-app-name>.azurewebsites.net/admin/host/systemkeys/eventgrid_extension"}]}
```
Use the value from above as the ```code=system-key``` in below set of commands.
Open [Azure Cloud Shell](https://shell.azure.com) and execute below commands.

```
storageName= <storage-account-name>
endpoint='https://<function-app-name>.azurewebsites.net/runtime/webhooks/eventgrid?functionName=blobEGTrigger&code=<system-key>'
resourceGroup=resource-group-name
storageid=$(az storage account show --name $storageName --resource-group $resourceGroup --query id --output tsv)
az eventgrid event-subscription create \
  --source-resource-id $storageid \
  --name vid-to-gif-function-app \
  --endpoint $endpoint \
  --subject-begins-with '/blobServices/default/containers/uploads'
```
## Upload the Videos
Upload a video to "uploads" container in your blob storage account.Wait for couple seconds and you should have a images extracted in "images" blob container.  