async function update_label_panel(labels) {
  let container = document.getElementById("labels");
  while (container.firstChild) {
    container.removeChild(container.firstChild);
  }
  for (let label of labels.reverse()) {
    let l = await fetch("/label/" + label.id + "?only_path=1", {});
    let label_response = await l.json();
    let a = document.createElement("a");
    let img = document.createElement("img");
    let cross_a = document.createElement("a");
    let cross = document.createElement("img");
    a.className = "label";
    cross.src = "/static/cross.png";
    cross.className = "cross";
    img.src = label_response.path;
    img.style.width = "100px";
    a.append(img);
    cross_a.append(cross);
    a.append(cross_a);
    container.append(a);
  }
}

$(document).ready(function() {
  (async () => {
    let response = await fetch("/labels");
    let labels = await response.json();
    await update_label_panel(labels);
    setInterval(async() => {
      let new_response = await fetch("/labels");
      let new_labels = await new_response.json();
      if (
        new_labels[new_labels.length - 1] != labels.length[labels.length - 1]
        && new_labels.length != labels.length
      ) {
        await update_label_panel(new_labels);
      }
    }, 60000);
  })();
});
