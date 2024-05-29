var form_label
var datasetIds
function add_dataset_button(e) {
    const dataset_container = document.getElementById("dataset-holder")

    const add_dataset_input = document.getElementById("add-dataset-source")
    const dataset_id = add_dataset_input.value

    
    
    if (dataset_id.substring(0, 5) != "prsc_") {
        
        alert("Wrong dataset id!")
        return
    }
    else if (isAlreadyAdded(dataset_id))
    {
        alert("Dataset already added!")
        return
    }

    const div_container = document.createElement("li")

        const input_tag = document.createElement("input")
        input_tag.classList.add("dataset_id")
        input_tag.type = "checkbox"
        input_tag.name = dataset_id
        input_tag.id = dataset_id
        input_tag.checked = true

    div_container.appendChild(input_tag)

        const label_tag = document.createElement("label")
        label_tag.htmlFor  = dataset_id
        label_tag.innerHTML = dataset_id

    div_container.appendChild(label_tag)
    
    dataset_container.appendChild(div_container)

    check_if_added()
}

function check_if_added() {
    let datasetsIds = document.getElementsByClassName("dataset_id")
    if (datasetsIds.length != 0) {
        form_label.innerHTML = "Selected datasets" 
    }
}

function isAlreadyAdded(idToCheck) {
    let datasetsIds = document.getElementsByClassName("dataset_id")
    if (datasetsIds == null) return false;

    for (var dataset_id of datasetsIds) {
        if (dataset_id.name == idToCheck) {
            return true;
        }
    }
    return false;
}
   


function main() {
    const add_button = document.getElementById("add-dataset")
    form_label = document.getElementById("form-header")
    check_if_added()
    add_button.addEventListener("click", add_dataset_button)
}

window.addEventListener("DOMContentLoaded", main)