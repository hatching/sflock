function greet(name) {
    return "Hello " + name;
}

var who = "World";
console.log(greet(who));

var show = false;
if (show) {
    alert(greet(who));
}
