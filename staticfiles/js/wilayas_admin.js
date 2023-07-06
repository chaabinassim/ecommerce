
$(document).ready(function(){

    var ul = document.getElementsByClassName("object-tools")[0];
    var li = document.createElement("li");
    var a = document.createElement("a")
    a.setAttribute('href','/delivery/update_wilayas')
    li.appendChild(a)
    a.appendChild(document.createTextNode("upload from yalidine"))
    ul.appendChild(li);
  });