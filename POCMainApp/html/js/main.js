session.subscribeToEvent("MyFriend/LauncherForAdultKnown", function (value) {
    console.log("From Event raised!")
    launcherForAdults(value);
});
session.subscribeToEvent("MyFriend/LauncherForAdultUnknown", function (value) {
    console.log("Event raised!")
    launcherForAdults(value);
});

session.subscribeToEvent("MyFriend/LauncherForKids", function (value) {
    console.log("Event raised!")
    launcherForKids(value);
});

function launcherForAdults(value) {

    document.getElementById("item_adult").style.visibility = 'visible';
    document.getElementById("item_kids").style.visibility= 'hidden';
    document.body.style.background='#eee';
    // document.body.style.backgroundImage='url(images/baloon.jpg)';
    // document.body.style.backgroundRepeat='no-repeat';
    // document.body.style.backgroundSize='100%';

}
function launcherForKids(value) {
    console.log("kids launcher")
    document.getElementById("item_kids").style.visibility = 'visible';
    document.getElementById("item_adult").style.visibility = 'hidden';
    document.body.style.backgroundImage='url(images/baloon.jpg)';
    // document.body.style.backgroundRepeat='';
    document.body.style.backgroundSize='100%';

}

function raiseEvent(value){
    session.raiseEvent("MyFriend/ChosenApp",value);

}


function exit()
{
   session.raiseEvent("MyFriend/ExitApp", 1);
}