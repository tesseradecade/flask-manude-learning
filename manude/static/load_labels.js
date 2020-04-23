async function update_label_panel(labels) {
  let container = document.getElementById("labels");
  while (container.firstChild) {
    container.removeChild(container.firstChild);
  }
  for (let label of labels.reverse()) {
    let l = await fetch("/label/" + label.id + "?only_path=1", {});
    let label_response = await l.json();
    let img = document.createElement("img");
    img.src = label_response.path;
    img.style.width = "100px";
    container.append(img);
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
