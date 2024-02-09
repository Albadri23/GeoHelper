const addbtn = document.querySelector(".add");
const input = document.querySelector(".in-g");


function removeInput(){
    this.parentElement.remove();
}




function addInput(){
    const easting = document.createElement("input");
    easting.type = "text";
    easting.placeholder = "Easting";
    easting.name = "east";

    const northing = document.createElement("input");
    northing.type = "text";
    northing.placeholder = "Northing";
    northing.name = "north";

    const btn = document.createElement("a");
    btn.className = "delete";
    btn.innerHTML = "&times";


    btn.addEventListener("click", removeInput);

    const flex = document.createElement("div");
    flex.className = "flex";

    input.appendChild(flex);
    flex.appendChild(easting);
    flex.appendChild(northing);
    flex.appendChild(btn);


}

addbtn.addEventListener("click", addInput);
