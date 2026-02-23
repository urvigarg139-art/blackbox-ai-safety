function scan(){

loader.style.display="block";

fetch("/scan",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({code:code.value})
})
.then(r=>r.json())
.then(d=>{

loader.style.display="none";
score.innerHTML="Risk Score: "+d.score;
issues.innerHTML=d.issues.join("<br>");

new Chart(pie,{
type:"doughnut",
data:{
labels:["Critical","High","Medium","Low"],
datasets:[{
data:[d.critical,d.high,d.medium,d.low]
}]
}
});
});
}