// let counter = 0;

if (!localStorage.getItem('counter')) {
    localStorage.setItem('counter', 0);
}

function count() {
    let counter = localStorage.getItem('counter');
    counter ++;
    // alert(counter);
    // if (counter % 10 === 0) {
    //     alert(`Count is not ${counter}`)
    // }

    document.querySelector('h1').innerHTML = counter;
    localStorage.setItem('counter', counter);
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('h1').innerHTML = localStorage.getItem('counter');
    // Set the value of the onclick button to the function count. 
    document.querySelector('button').onclick = count;
    // great way to call a function every second
    // setInterval(count, 1000);
});