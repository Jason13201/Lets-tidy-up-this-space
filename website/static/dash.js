$("#person-select").dropdown();

const sortable = new Draggable.Sortable(document.querySelectorAll("ul"), {
  draggable: "li",
});
