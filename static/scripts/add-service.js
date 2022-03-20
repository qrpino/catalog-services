resources_data = {};
resourcesDiv = document.querySelector("#resources_div");
withdrawResourceButton = document.querySelector("#withdraw-resource-button");
addResourceButton = document.querySelector("#add-resource-button");
function withdrawResourceInput()
{
    if(resourcesDiv.childElementCount > 2)
    {
        resourcesDiv.removeChild(resourcesDiv.lastChild);
    }
}
function addResourceInput()
{
    newSelect = document.createElement("select");
    newSelect.setAttribute("name", "resources_needed_" + String(resourcesDiv.childElementCount + 1));
    for(resource in resources_data)
    {
        newOption = document.createElement("option");
        newOption.setAttribute("value", newOption['id']);
        newOption.value = resource['name'];
        newSelect.appendChild(newOption);
    }
    resourcesDiv.appendChild(newSelect);
}
/*
addResourceInput = document.createElement("button");
divToAppend = document.querySelector('#resources_div');
selectToListen = document.querySelector('#select_resource_1');
*/