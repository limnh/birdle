'use strict';

let numWrong = 0;
// let correctGuesses = 0;



const button = document.querySelector('#submit-guess');


button.addEventListener('click', () => {
  const userGuess = document.querySelector('#guess').value;

  fetch(`/submit-guess?guess=${userGuess}`)
  .then((response) => response.text())
  .then((serverData) => {
    console.log(serverData)
    document.querySelector('#guess').innerHTML = serverData;
  }); 
});