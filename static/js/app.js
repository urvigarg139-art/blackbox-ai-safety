function scan(){

fetch("/scan",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({code:document.getElementById("code").value})
})
.then(r=>r.json())
.then(d=>{
score.innerHTML="Risk: "+d.score+"%";
issues.innerHTML="Issues: "+d.issues.join(", ");
cat.innerHTML="Categories: "+d.category.join(", ");

fetch("/history")
.then(r=>r.json())
.then(h=>{
let html="";
h.forEach(x=>html+=`Score ${x[0]} at ${x[1]}<br>`);
history.innerHTML=html;
});
});
}