


var btn1 = document.getElementById('btn1');
var btn2 = document.getElementById('btn2');

function addButton(){
    // Get the div that the buttons will exist in
    container = document.getElementById('type-button-container');
    //create <p></p>
    btn = document.createElement('p');
    //create text element of p tag
    txt = document.createTextNode('btn');
    //combine text and p
    btn.appendChild(txt);
    //put the <p> in to the <div>
    container.appendChild(btn);
}

// addButton();

// Toggles between the two buttons, this is the set up for building the
// tabs that will changing the defense typing based on certain abilities

// Give certain abilities id based on a predetermined list I'll have to make
// If those abilities are on the page then add the buttons





//Toggling between 2 buttons
// btn1.style.display = 'None';
// btn2.style.display = 'None';

// btn1.addEventListener('click', function(){
//     if (btn1.classList.contains('fire-type') == false){
//         btn1.classList.toggle('fire-type');
//         if (btn2.classList.contains('water-type') == true){
//             btn2.classList.toggle('water-type');
//         }
//     }
// });

// btn2.addEventListener('click', function(){
//     if (btn2.classList.contains('water-type') == false){
//         btn2.classList.toggle('water-type');
//         if (btn1.classList.contains('fire-type') == true){
//             btn1.classList.toggle('fire-type');
//         }
//     }
// });
