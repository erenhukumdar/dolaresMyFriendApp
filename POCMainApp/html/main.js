session.subscribeToEvent("MyFriend/PrintTime", function (value) {
    console.log("From Event raised!")
    printTime(value);
});
session.subscribeToEvent("MyFriend/FinishTime", function (value) {
    console.log("Event raised!")
    printFinish(value);
});

function printTime(value) {

    document.getElementById("start").innerHTML = value;
}
function printFinish(value) {

    document.getElementById("finish").innerHTML = value;

}
