const btn =
document.getElementById(
"summaryBtn"
);

const result =
document.getElementById(
"summaryResult"
);

let summaryLoaded = false;


if (btn && result) {

btn.addEventListener(

"click",

function () {


// Hide if already visible
if (
result.style.display ===
"block"
) {

result.style.display =
"none";

btn.innerText =
"Summarize Blog";

return;

}


// Show existing summary
if (
summaryLoaded
) {

result.style.display =
"block";

btn.innerText =
"Hide Summary";

return;

}


// First fetch
fetch(
`/blogs/summary/${blogSlug}/`
)

.then(
response =>
response.json()
)

.then(data => {

result.innerHTML =

`
<h4>Summary</h4>

<p>
${data.summary}
</p>
`;

result.style.display =
"block";

btn.innerText =
"Hide Summary";

summaryLoaded =
true;

})

.catch(error => {

console.log(
error
);

result.innerHTML =

`
<p>
Unable to generate summary.
</p>
`;

result.style.display =
"block";

});

}

);

}