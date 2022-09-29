var today = new Date();
var date = today.getTime()
document.getElementById("currentDate").innerText = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();