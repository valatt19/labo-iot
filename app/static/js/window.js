
const socket = io();
socket.on("update", update);

///////////////////////////////////////
// UPDATE when new measures received //
///////////////////////////////////////
function update(is_open, temp_in, temp_out, hum, current) {
    var window_info = document.getElementById("window_info");
    var window_img = document.getElementById("window_img");

    if (is_open) {
        window_info.innerHTML = "La fenêtre est ouverte"
        window_img.src = "../static/image/window_open.png"
        window_img.alt = "open"
    } else {
        window_info.innerHTML = "La fenêtre est fermée"
        window_img.src = "../static/image/window_close.png"
        window_img.alt = "closed"
    }

    var myTable = document.getElementById("measures");
    myTable.rows[0].cells[1].innerHTML = temp_in.toFixed(1) + " °C";
    myTable.rows[1].cells[1].innerHTML = temp_out.toFixed(1) + " °C";
    myTable.rows[2].cells[1].innerHTML = hum.toFixed(2) + " %";
    myTable.rows[3].cells[1].innerHTML = current;
}
