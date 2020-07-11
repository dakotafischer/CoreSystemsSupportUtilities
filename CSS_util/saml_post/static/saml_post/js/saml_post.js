
function addAttribute() {
    //add two text fields for attribute name and attribute value

    // find out which attribute we're on by checking the number in the lastAttribute element
    //var lastAttributeCopy = document.getElementById("lastAttribute")
    //var lastAttribute = document.getElementById("lastAttribute").textContent;
    //var attributeNumber = Number(lastAttribute[lastAttribute.lastIndexOf('#') + 1]);

    // I think a better way of doing that is just to have a hidden attribute_count input field
    var attributeNumber = Number(document.getElementById("attribute_count").value)
    document.getElementById("attribute_count").value = attributeNumber + 1


    // create a new <p> Attribute NumberX:</p> and give it the lastAttribute id
    var container = document.getElementById("container");
    var newParagraph = document.createElement("p")
    newParagraph.textContent = "Attribute #" + (attributeNumber+1);
    // make this the new lastAttribute element for the next time the button is pushed
    document.getElementById("lastAttribute").id = "removed";
    newParagraph.id = "lastAttribute";
    container.appendChild(newParagraph);

    // add attribute_name label and input elements to get the attribute name info
    var newAttributeName = "attribute_name_" + String(attributeNumber);
    var label = document.createElement("label");
    label.textContent = "Name: ";
    label.id = newAttributeName;
    label.htmlFor = newAttributeName;
    var input = document.createElement("input");
    input.type = "text";
    input.name = newAttributeName;
    input.id = newAttributeName;
    container.appendChild(label);
    container.appendChild(input);
    container.appendChild(document.createElement("br"));

    // add attribute_value label and input elements to get the attribute value info
    var newAttributeValue = "attribute_value_" + String(attributeNumber);
    var label = document.createElement("label");
    label.textContent = "Value: ";
    label.id = newAttributeValue;
    label.htmlFor = newAttributeValue;
    var input = document.createElement("input");
    input.type = "text";
    input.name = newAttributeValue;
    input.id = newAttributeValue;
    container.appendChild(label);
    container.appendChild(input);
    container.appendChild(document.createElement("br"));
}
/*
        <label for="attribute_name">   Name: </label>
        <input type="text" name="attribute_name" id="attribute_name"  value="{{ fields.attribute_name }}"><br>
        <label for="attribute_value">   Value: </label>
        <input type="text" name="attribute_value" id="attribute_value" value="{{ fields.attribute_value}}"><br>
*/

function updateOpenBtnText(updateText) {
    //updates the text in the openbtn and prepends the logo
    logo = document.getElementById("paul");
    document.getElementById("openbtn").textContent = String(updateText);
    document.getElementById("openbtn").prepend(logo);
}

function openNav() {
//document.getElementById("mySidebar").style.width = "250px";
//document.getElementById("main").style.marginLeft = "250px";
if (document.getElementById("main").isOpen == null || document.getElementById("main").isOpen == false) {
    document.getElementById("mySidebar").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";
    document.getElementById("main").isOpen = true;
    updateOpenBtnText("Close Menu")
    //logo = document.getElementById("paul");
    //document.getElementById("openbtn").textContent = "Close Menu";
    //document.getElementById("openbtn").prepend(logo);
    console.log("It was closed, now it's open!");
} else {
    closeNav();
    //document.getElementById("mySidebar").style.width = "0";
    //document.getElementById("main").style.marginLeft= "0";
    //document.getElementById("main").isOpen = false;
    //console.log("It was open, now it's closed!")
}
//document.getElementById("main").isOpen = true
}

function closeNav() {
    document.getElementById("mySidebar").style.width = "0";
    document.getElementById("main").style.marginLeft= "0";
    document.getElementById("main").isOpen = false;
    updateOpenBtnText("Menu");
    console.log("It was open, now it's closed!");
}

function highlight(e) {
  if (selected[0]) {
    selected[0].className = 'profileRecord';
  }
  e.target.parentNode.className = 'selected';
}

var table = document.getElementById('profileTable'),
selected = table.getElementsByClassName('selected');
table.onclick = highlight;

function loadProfile() {
    selected = table.getElementsByClassName('selected')[0];
    if (selected == undefined) {
        //tell user to select something
        alert('Select a Profile to Load or choose "Start from Scratch"')
    }
    profile_url = selected.firstElementChild.textContent;
    //location.href='https://google.com';
    location.href = profile_url;
    // this should redirect to /saml_post/ + the profile id that the user selected
}