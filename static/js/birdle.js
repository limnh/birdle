'use strict';

const button = document.querySelector('#submit-guess');

button.addEventListener('click', () => {
  const userGuess = document.querySelector('#guess').value;

  fetch(`/submit-guess?guess=${userGuess}`)
  .then((response) => {
    return response.json()
  })
  .then((body) => {
    document.querySelector('#guess-form').innerHTML = body.status

    const isComName = body.answer.com_name == body.guess.com_name
    if(isComName === true) {
      document.querySelector("#comname").style.backgroundColor = "green";
    } else {
      document.querySelector("#comname").style.backgroundColor = "red"
    }

    const isOrder = body.answer.order == body.guess.order
    if(isOrder === true) {
      document.querySelector("#order").style.backgroundColor = "green";
    } else {
      document.querySelector("#order").style.backgroundColor = "red"
    }

    const isFamilyComName = body.answer.family_com_name == body.guess.family_com_name
    if(isFamilyComName === true) {
      document.querySelector("#family").style.backgroundColor = "green";
    } else {
      document.querySelector("#family").style.backgroundColor = "red"
    }
  })
});
