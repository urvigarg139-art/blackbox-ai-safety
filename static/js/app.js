let txt="Paste your source code and BlackBox will detect vulnerabilities.";
let i=0;

setInterval(()=>{
if(i<txt.length){
document.getElementById("type").innerHTML+=txt[i];
i++;
}
},40);

function runAudit(){

let text=document.getElementById("input").innerText;

fetch("/audit",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({data:text})
})
.then(res=>res.json())
.then(d=>{

document.getElementById("result").innerHTML=
`<b>Language:</b> ${d.language}<br>
<b>Threat Level:</b> ${d.result}<br>
<b>Confidence:</b> ${d.confidence}%<br><br>
<b>Issues:</b><br>${d.issues.join("<br>")}<br><br>
<b>Fixes:</b><br>${d.fixes.join("<br>")}`;

document.getElementById("fill").style.width=d.confidence+"%";

});
}