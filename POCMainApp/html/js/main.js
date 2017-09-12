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


session.subscribeToEvent("MyFriend/OpenLauncherForKids", function (value) {
    console.log("Event raised!")
    launcherForKids(value);
    funFunction(value);
});

function launcherForAdults(value) {
  console.log("adult launcher");
    document.getElementById("adultLauncher").style.display = 'block';
    document.getElementById("kidsLauncher").style.display= 'none';
    // document.body.style.background='#eee';
    // document.body.style.backgroundImage='url(images/baloon.jpg)';
    // document.body.style.backgroundRepeat='no-repeat';
    // document.body.style.backgroundSize='100%';

}
function backFunction(value) {
  launcherForAdults(value);
    session.raiseEvent("MyFriend/BackPressed",value);
}
function launcherForKids(value) {
    console.log("kids launcher");
 document.getElementById("adultLauncher").style.display = 'none';
    document.getElementById("kidsLauncher").style.display= 'block';
    // document.body.style.backgroundImage='url(images/baloon.jpg)';
    // document.body.style.backgroundRepeat='';
    //document.body.style.backgroundSize='100%';

}
function launcherForKids2(value) {
    console.log("kids launcher");
 document.getElementById("adultLauncher").style.display = 'none';
    document.getElementById("kidsLauncher").style.display= 'block';
    funFunction (value) ;


    // document.body.style.backgroundImage='url(images/baloon.jpg)';
    // document.body.style.backgroundRepeat='';
    //document.body.style.backgroundSize='100%';

}
function raiseEvent(value){
    session.raiseEvent("MyFriend/ChosenApp",value);

}

function safeFunction(value){
    session.raiseEvent("MyFriend/UnderConstruction",value);

}
function  funFunction(value) {
    session.raiseEvent("MyFriend/KidsFun",value);

}

function exit()
{
   session.raiseEvent("MyFriend/ExitApp", 1);
}