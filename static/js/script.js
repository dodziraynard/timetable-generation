// Slots
const addButton = document.querySelector('#add-slot-button');
const rowTemplate = document.querySelector('#slot-row-template');
const rowsContainer = document.querySelector('#slot-rows-container');
const removeButtons = document.querySelectorAll('.remove-button');

addButton?.addEventListener('click', () => {
  const row = rowTemplate.content.cloneNode(true);
  rowsContainer.appendChild(row);

  // Attache event listener to the new remove button
  rowsContainer.querySelectorAll('.remove-button').forEach(button => {
    button.addEventListener('click', () => {
      button.parentElement.parentElement.remove();
    })
  })
})

removeButtons?.forEach(button => {
  button.addEventListener('click', () => {
    button.parentElement.parentElement.remove();
  })
})

// EVents
const addEventButton = document.querySelector('#add-event-button');
const eventRowTemplate = document.querySelector('#event-row-template');
const eventRowsContainer = document.querySelector('#event-rows-container');
addEventButton?.addEventListener('click', () => {
  const row = eventRowTemplate.content.cloneNode(true);
  eventRowsContainer.appendChild(row);

  // Attache event listener to the new remove button
  eventRowsContainer.querySelectorAll('.remove-button').forEach(button => {
    button.addEventListener('click', () => {
      button.parentElement.parentElement.remove();
    })
  })
})
